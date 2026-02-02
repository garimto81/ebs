#!/usr/bin/env python3
"""PDF 분할 도구 - 큰 PDF를 여러 파일로 분할"""

import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def split_pdf(input_path: str, pages_per_file: int = 20) -> list[str]:
    """PDF를 지정된 페이지 수로 분할

    Args:
        input_path: 원본 PDF 경로
        pages_per_file: 파일당 페이지 수 (기본 20)

    Returns:
        생성된 파일 경로 목록
    """
    input_file = Path(input_path)
    output_dir = input_file.parent / f"{input_file.stem}_split"
    output_dir.mkdir(exist_ok=True)

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    print(f"총 {total_pages}페이지, {pages_per_file}페이지씩 분할")

    output_files = []
    for start in range(0, total_pages, pages_per_file):
        end = min(start + pages_per_file, total_pages)
        writer = PdfWriter()

        for page_num in range(start, end):
            writer.add_page(reader.pages[page_num])

        output_file = output_dir / f"{input_file.stem}_p{start+1:03d}-{end:03d}.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)

        output_files.append(str(output_file))
        print(f"  생성: {output_file.name} (페이지 {start+1}-{end})")

    print(f"\n분할 완료: {len(output_files)}개 파일 → {output_dir}")
    return output_files


def extract_pages(input_path: str, start: int, end: int, output_path: str = None) -> str:
    """특정 페이지 범위만 추출

    Args:
        input_path: 원본 PDF 경로
        start: 시작 페이지 (1부터)
        end: 끝 페이지 (포함)
        output_path: 출력 파일 경로 (없으면 자동 생성)
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num in range(start - 1, end):
        writer.add_page(reader.pages[page_num])

    if not output_path:
        input_file = Path(input_path)
        output_path = input_file.parent / f"{input_file.stem}_p{start}-{end}.pdf"

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"추출 완료: 페이지 {start}-{end} → {output_path}")
    return str(output_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법:")
        print("  분할: python split_pdf.py <pdf파일> [페이지수]")
        print("  추출: python split_pdf.py <pdf파일> --extract <시작> <끝>")
        print()
        print("예시:")
        print("  python split_pdf.py user-manual.pdf 20      # 20페이지씩 분할")
        print("  python split_pdf.py user-manual.pdf --extract 1 30  # 1-30페이지 추출")
        sys.exit(1)

    input_file = sys.argv[1]

    if len(sys.argv) >= 3 and sys.argv[2] == "--extract":
        start = int(sys.argv[3])
        end = int(sys.argv[4])
        extract_pages(input_file, start, end)
    else:
        pages = int(sys.argv[2]) if len(sys.argv) >= 3 else 20
        split_pdf(input_file, pages)
