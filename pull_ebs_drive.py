#!/usr/bin/env python3
"""
pull_ebs_drive.py -- EBS Drive->로컬 역방향 동기화

MAPPING_ngd.json의 prd_registry 기반으로 Drive 수정 시각과 로컬 수정 시각을
비교하여 Drive가 더 최신인 경우 내용을 내려받고 차이를 출력합니다.

실행:
    cd C:\claude && python ebs/pull_ebs_drive.py              # 상태 확인 + 변경 diff 출력
    cd C:\claude && python ebs/pull_ebs_drive.py --dry-run    # 시각 비교만 (다운로드 없음)
    cd C:\claude && python ebs/pull_ebs_drive.py --force      # 시각 무관 강제 pull
    cd C:\claude && python ebs/pull_ebs_drive.py --apply      # 변경사항 로컬 파일에 적용
"""
import sys
import json
import os
import argparse
import difflib
import logging
import re
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "C:/claude")

from lib.google_docs.auth import get_credentials
from googleapiclient.discovery import build

EBS_ROOT = "1GlDqSgEDs9z8j5VY6iX3QndTLb6_8-PF"
MAPPING_FILE = r"C:\claude\ebs\docs\MAPPING_ngd.json"
LOG_DIR = Path(r"C:\claude\ebs\logs")


def setup_logging(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"pull-{datetime.now().strftime('%Y-%m-%d')}.log"

    logger = logging.getLogger("ebs_pull")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def get_drive_modified_time(drive_service, file_id: str) -> datetime:
    """Drive 파일 수정 시각 조회 (UTC)"""
    result = drive_service.files().get(fileId=file_id, fields="modifiedTime").execute()
    dt_str = result.get("modifiedTime", "1970-01-01T00:00:00Z")
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def get_local_modified_time(local_path: str) -> datetime:
    """로컬 파일 수정 시각 조회 (UTC 변환)"""
    mtime = os.path.getmtime(local_path)
    return datetime.fromtimestamp(mtime, tz=timezone.utc)


def export_doc_as_text(drive_service, file_id: str) -> str:
    """Google Docs를 plain text로 내보내기"""
    response = drive_service.files().export(
        fileId=file_id,
        mimeType="text/plain",
    ).execute()
    # export() returns bytes
    if isinstance(response, bytes):
        return response.decode("utf-8", errors="replace")
    return str(response)


def text_to_markdown_lines(text: str) -> list[str]:
    """
    Google Docs plain text export를 markdown과 비교 가능한 형태로 정규화.
    - 연속 공백 라인 제거
    - 앞뒤 공백 트림
    """
    lines = text.splitlines()
    normalized = []
    prev_blank = False
    for line in lines:
        stripped = line.rstrip()
        is_blank = stripped == ""
        if is_blank and prev_blank:
            continue  # 연속 공백 제거
        normalized.append(stripped)
        prev_blank = is_blank
    return normalized


def read_local_as_lines(local_path: str) -> list[str]:
    """로컬 markdown 파일을 라인 목록으로 읽기"""
    with open(local_path, encoding="utf-8") as f:
        return [line.rstrip() for line in f.readlines()]


def show_diff(local_lines: list[str], drive_lines: list[str], prd_id: str) -> int:
    """unified diff 출력. 변경 라인 수 반환"""
    diff = list(difflib.unified_diff(
        local_lines,
        drive_lines,
        fromfile=f"{prd_id} (로컬)",
        tofile=f"{prd_id} (Drive)",
        lineterm="",
    ))
    if not diff:
        return 0
    print("\n" + "=" * 60)
    print(f"  {prd_id} DIFF (로컬 → Drive)")
    print("=" * 60)
    # 최대 200줄만 표시
    shown = diff[:200]
    print("\n".join(shown))
    if len(diff) > 200:
        print(f"  ... (+{len(diff) - 200} 라인 생략) ...")
    print("=" * 60)
    changes = sum(1 for l in diff if l.startswith("+") or l.startswith("-"))
    return changes


def apply_drive_content(local_path: str, drive_text: str, logger: logging.Logger):
    """
    Drive 텍스트를 로컬 파일에 적용.
    주의: plain text 변환으로 인해 Markdown 포맷 손실 가능.
    로컬 파일 백업 후 적용.
    """
    backup_path = local_path + ".bak"
    with open(local_path, encoding="utf-8") as f:
        original = f.read()
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(original)
    logger.info(f"백업 저장: {backup_path}")

    with open(local_path, "w", encoding="utf-8") as f:
        f.write(drive_text)
    logger.info(f"Drive 내용 적용 완료: {local_path}")


def pull_prd(
    drive_service,
    prd_id: str,
    prd_info: dict,
    dry_run: bool,
    force: bool,
    apply: bool,
    logger: logging.Logger,
) -> bool:
    """단일 PRD pull. True = 성공 또는 최신"""
    doc_id = prd_info["doc_id"]
    display_name = prd_info["display_name"]
    local_file = prd_info["local_file"]

    if not os.path.exists(local_file):
        logger.warning(f"{prd_id}: 로컬 파일 없음 -> {local_file}")
        return False

    local_mtime = get_local_modified_time(local_file)
    drive_mtime = get_drive_modified_time(drive_service, doc_id)

    local_str = local_mtime.strftime("%Y-%m-%d %H:%M:%S UTC")
    drive_str = drive_mtime.strftime("%Y-%m-%d %H:%M:%S UTC")

    logger.info(f"{prd_id}: 로컬={local_str} / Drive={drive_str}")

    if not force and drive_mtime <= local_mtime:
        logger.info(f"{prd_id}: 로컬이 최신 -> 스킵 ({display_name})")
        return True

    reason = "강제 pull" if force else "Drive 수정 감지"
    logger.info(f"{prd_id}: {reason} ({display_name})")

    if dry_run:
        logger.info(f"{prd_id}: [DRY-RUN] 다운로드 건너뜀")
        return True

    # Drive에서 plain text 내보내기
    logger.info(f"{prd_id}: Drive에서 텍스트 내보내는 중...")
    drive_text = export_doc_as_text(drive_service, doc_id)
    drive_lines = text_to_markdown_lines(drive_text)
    local_lines = read_local_as_lines(local_file)

    change_count = show_diff(local_lines, drive_lines, prd_id)

    if change_count == 0:
        logger.info(f"{prd_id}: 내용 동일 (시각만 다름)")
        return True

    logger.info(f"{prd_id}: {change_count}개 라인 변경 감지")

    if apply:
        apply_drive_content(local_file, drive_text, logger)
    else:
        logger.info(
            f"{prd_id}: --apply 플래그 없음 -> 로컬 파일 유지 (diff만 출력됨)"
        )

    return True


def main():
    parser = argparse.ArgumentParser(description="EBS Drive->로컬 역방향 동기화")
    parser.add_argument("--dry-run", action="store_true", help="시각 비교만 (다운로드 없음)")
    parser.add_argument("--force", action="store_true", help="시각 무관 강제 pull")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Drive 내용을 로컬 파일에 실제 적용 (주의: Markdown 포맷 손실 가능)",
    )
    parser.add_argument("--prd", type=str, help="특정 PRD ID만 처리 (예: PRD-0002)")
    args = parser.parse_args()

    logger = setup_logging(LOG_DIR)
    logger.info("=== EBS Drive->로컬 Pull 시작 ===")
    if args.dry_run:
        logger.info("[DRY-RUN 모드]")
    if args.force:
        logger.info("[FORCE 모드]")
    if args.apply:
        logger.info("[APPLY 모드] Drive 내용을 로컬에 적용합니다")

    with open(MAPPING_FILE, encoding="utf-8") as f:
        mapping = json.load(f)

    prd_registry = mapping.get("prd_registry", {})
    if not prd_registry:
        logger.error("MAPPING_ngd.json에 prd_registry가 없습니다.")
        return 1

    # 특정 PRD 필터
    if args.prd:
        if args.prd not in prd_registry:
            logger.error(f"{args.prd}: 레지스트리에 없음. 사용 가능: {list(prd_registry.keys())}")
            return 1
        prd_registry = {args.prd: prd_registry[args.prd]}

    creds = get_credentials()
    drive_service = build("drive", "v3", credentials=creds)

    success = 0
    total = len(prd_registry)

    for prd_id, prd_info in prd_registry.items():
        if pull_prd(drive_service, prd_id, prd_info, args.dry_run, args.force, args.apply, logger):
            success += 1

    logger.info(f"=== Pull 완료: {success}/{total} ===")
    if not args.apply and not args.dry_run:
        logger.info("변경사항을 적용하려면 --apply 플래그를 추가하세요.")
    return 0 if success == total else 1


if __name__ == "__main__":
    sys.exit(main())
