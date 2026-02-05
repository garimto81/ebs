#!/usr/bin/env python3
"""
EBS Google Drive Organizer

Google Drive의 EBS 폴더 구조를 관리하는 CLI 도구입니다.

Usage:
    python tools/gdrive_organizer.py status              # 현재 상태 조회
    python tools/gdrive_organizer.py create-folder NAME  # 폴더 생성
    python tools/gdrive_organizer.py move FILE_ID FOLDER # 파일 이동
    python tools/gdrive_organizer.py --dry-run ...       # 미리보기 (실행 안함)
"""

import argparse
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lib.google_docs.auth import get_credentials
from googleapiclient.discovery import build


# EBS Folder IDs (folder names have numeric prefix for ordering: 1-phase-0, 2-phase-1, etc.)
FOLDER_IDS = {
    "root": "1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF",
    "1-phase-0": "1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS",
    "2-phase-1": "18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s",
    "3-phase-2": "1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-",
    "4-phase-3": "1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k",
    "5-operations": "1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-",
    # Aliases for convenience
    "phase-0": "1AKvKghcaorH5A-kg9pD4rHxF5ueQWJgS",
    "phase-1": "18Oz-iP3JIEQgjG-x-3zhW1RJfODrnh5s",
    "phase-2": "1d3R2gdhJrUKTEzxBKng8VTR9Dv3qxBi-",
    "phase-3": "1-4o14wikrZcSYCH8Y0gMT5drXQ5h5V7k",
    "operations": "1fKZLKl5K7xEPsD1lXntxWTHBTSbIJo8-",
}


def get_drive_service():
    """Google Drive API 서비스 객체 반환"""
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)


def list_folder_contents(drive, folder_id: str) -> list:
    """폴더 내용 조회"""
    results = drive.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id, name, mimeType)",
        orderBy="name",
    ).execute()
    return results.get("files", [])


def cmd_status(args):
    """현재 EBS 폴더 구조 상태 출력"""
    drive = get_drive_service()

    print("=== EBS Google Drive Structure ===")
    print()

    for folder_name, folder_id in FOLDER_IDS.items():
        files = list_folder_contents(drive, folder_id)

        # Count folders and documents
        folders = [f for f in files if "folder" in f["mimeType"]]
        docs = [f for f in files if "folder" not in f["mimeType"]]

        display_name = f"EBS/{folder_name}/" if folder_name != "root" else "EBS/"
        print(f"{display_name} ({len(docs)} docs, {len(folders)} folders)")
        print(f"  ID: {folder_id}")

        for f in docs:
            print(f"    [DOC] {f['name']}")
        for f in folders:
            print(f"    [FOLDER] {f['name']}")
        print()

    print("=== Status: OK ===")


def cmd_create_folder(args):
    """EBS 폴더 내에 새 폴더 생성"""
    drive = get_drive_service()
    folder_name = args.name
    parent = args.parent or "root"

    parent_id = FOLDER_IDS.get(parent, parent)

    if args.dry_run:
        print(f"[DRY-RUN] Would create folder '{folder_name}' in {parent} ({parent_id})")
        return

    # Check if folder already exists
    query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive.files().list(q=query, fields="files(id, name)").execute()
    existing = results.get("files", [])

    if existing:
        print(f"[EXISTS] {folder_name}: {existing[0]['id']}")
        return

    # Create folder
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = drive.files().create(body=metadata, fields="id").execute()
    print(f"[CREATED] {folder_name}: {folder.get('id')}")


def cmd_move(args):
    """파일을 다른 폴더로 이동 (ID 보존)"""
    drive = get_drive_service()
    file_id = args.file_id
    target = args.target

    target_id = FOLDER_IDS.get(target, target)

    # Get current parents
    file_info = drive.files().get(fileId=file_id, fields="name, parents").execute()
    file_name = file_info.get("name", "Unknown")
    previous_parents = ",".join(file_info.get("parents", []))

    if args.dry_run:
        print(f"[DRY-RUN] Would move '{file_name}' ({file_id})")
        print(f"          From: {previous_parents}")
        print(f"          To: {target} ({target_id})")
        return

    # Move file
    drive.files().update(
        fileId=file_id,
        addParents=target_id,
        removeParents=previous_parents,
        fields="id, parents",
    ).execute()

    print(f"[MOVED] {file_name} -> {target}")


def cmd_list_docs(args):
    """모든 문서 목록과 ID 출력"""
    drive = get_drive_service()

    print("=== EBS Document List ===")
    print()

    all_docs = []
    for folder_name, folder_id in FOLDER_IDS.items():
        files = list_folder_contents(drive, folder_id)
        docs = [f for f in files if "folder" not in f["mimeType"]]

        for doc in docs:
            location = f"EBS/{folder_name}/" if folder_name != "root" else "EBS/"
            all_docs.append({
                "name": doc["name"],
                "id": doc["id"],
                "location": location,
            })

    for doc in all_docs:
        print(f"[{doc['location']}]")
        print(f"  Name: {doc['name']}")
        print(f"  ID: {doc['id']}")
        print(f"  URL: https://docs.google.com/document/d/{doc['id']}/edit")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="EBS Google Drive Organizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="미리보기 모드 (실제 변경 없음)",
    )

    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # status
    parser_status = subparsers.add_parser("status", help="현재 상태 조회")
    parser_status.set_defaults(func=cmd_status)

    # create-folder
    parser_create = subparsers.add_parser("create-folder", help="폴더 생성")
    parser_create.add_argument("name", help="폴더 이름")
    parser_create.add_argument(
        "--parent",
        default="root",
        help="부모 폴더 (root, phase-0, phase-1, operations 또는 ID)",
    )
    parser_create.set_defaults(func=cmd_create_folder)

    # move
    parser_move = subparsers.add_parser("move", help="파일 이동")
    parser_move.add_argument("file_id", help="이동할 파일 ID")
    parser_move.add_argument(
        "target",
        help="대상 폴더 (root, phase-0, phase-1, operations 또는 ID)",
    )
    parser_move.set_defaults(func=cmd_move)

    # list-docs
    parser_list = subparsers.add_parser("list-docs", help="문서 목록 조회")
    parser_list.set_defaults(func=cmd_list_docs)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
