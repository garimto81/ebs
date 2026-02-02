#!/usr/bin/env python3
"""
PDF 분할 도구 - 대용량 PDF를 작은 파일로 분할

Claude Code에서 대용량 PDF 처리 시 발생하는 문제 해결:
- 최대 100페이지 제한
- 30-32MB 파일 크기 제한
- 페이지당 1,500-3,000 토큰 제한

Usage:
    python pdf_splitter.py input.pdf                    # 기본 20페이지씩 분할
    python pdf_splitter.py input.pdf -p 10              # 10페이지씩 분할
    python pdf_splitter.py input.pdf -o output_dir      # 출력 디렉토리 지정
    python pdf_splitter.py input.pdf --text             # 텍스트 추출 모드
    python pdf_splitter.py input.pdf --text --chunks    # 청크 단위 텍스트 추출
"""

import argparse
import sys
from pathlib import Path
from typing import Generator

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF가 설치되지 않았습니다.")
    print("설치: pip install pymupdf")
    sys.exit(1)


def split_pdf(
    input_path: str,
    output_dir: str | None = None,
    pages_per_chunk: int = 20
) -> list[str]:
    """
    PDF를 지정된 페이지 수로 분할

    Args:
        input_path: 입력 PDF 파일 경로
        output_dir: 출력 디렉토리 (None이면 입력 파일과 같은 위치)
        pages_per_chunk: 청크당 페이지 수 (기본 20)

    Returns:
        생성된 파일 경로 목록
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_path}")

    if output_dir is None:
        output_dir = input_file.parent / f"{input_file.stem}_split"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(input_path)
    total_pages = len(doc)
    created_files = []

    print(f"입력 파일: {input_path}")
    print(f"총 페이지: {total_pages}")
    print(f"청크 크기: {pages_per_chunk}페이지")
    print(f"출력 디렉토리: {output_dir}")
    print("-" * 50)

    chunk_count = (total_pages + pages_per_chunk - 1) // pages_per_chunk

    for chunk_idx in range(chunk_count):
        start_page = chunk_idx * pages_per_chunk
        end_page = min(start_page + pages_per_chunk, total_pages)

        output_file = output_dir / f"{input_file.stem}_part{chunk_idx + 1:03d}.pdf"

        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)
        new_doc.save(str(output_file))
        new_doc.close()

        file_size = output_file.stat().st_size / 1024  # KB
        print(f"  생성: {output_file.name} (페이지 {start_page + 1}-{end_page}, {file_size:.1f}KB)")
        created_files.append(str(output_file))

    doc.close()

    print("-" * 50)
    print(f"완료: {len(created_files)}개 파일 생성")

    return created_files


def extract_text_by_page(pdf_path: str) -> Generator[tuple[int, str], None, None]:
    """
    페이지별 텍스트 추출 (메모리 효율적)

    Args:
        pdf_path: PDF 파일 경로

    Yields:
        (페이지 번호, 텍스트) 튜플
    """
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        yield page_num + 1, page.get_text()
    doc.close()


def extract_text_to_file(
    input_path: str,
    output_path: str | None = None,
    chunk_mode: bool = False,
    chunk_size: int = 2000,
    chunk_overlap: int = 500
) -> str:
    """
    PDF에서 텍스트 추출하여 파일로 저장

    Args:
        input_path: 입력 PDF 파일 경로
        output_path: 출력 텍스트 파일 경로 (None이면 자동 생성)
        chunk_mode: 청크 모드 활성화 (LLM 처리에 최적화)
        chunk_size: 청크 크기 (문자 수)
        chunk_overlap: 청크 오버랩 (문자 수)

    Returns:
        생성된 텍스트 파일 경로
    """
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {input_path}")

    if output_path is None:
        suffix = "_chunks.txt" if chunk_mode else ".txt"
        output_path = input_file.with_suffix(suffix)

    print(f"입력 파일: {input_path}")
    print(f"출력 파일: {output_path}")
    print(f"모드: {'청크 모드' if chunk_mode else '페이지 모드'}")
    print("-" * 50)

    doc = fitz.open(input_path)
    total_pages = len(doc)

    with open(output_path, "w", encoding="utf-8") as f:
        if chunk_mode:
            # 전체 텍스트를 청크로 분할
            full_text = ""
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                full_text += page.get_text() + "\n"
                print(f"  페이지 {page_num + 1}/{total_pages} 읽기 완료")

            # 청킹
            chunks = []
            start = 0
            chunk_idx = 0
            while start < len(full_text):
                end = start + chunk_size
                chunk = full_text[start:end]
                chunks.append(chunk)

                f.write(f"\n{'='*60}\n")
                f.write(f"CHUNK {chunk_idx + 1} (문자 {start}-{min(end, len(full_text))})\n")
                f.write(f"{'='*60}\n\n")
                f.write(chunk)

                start = end - chunk_overlap
                chunk_idx += 1

            print(f"  총 {len(chunks)}개 청크 생성")
        else:
            # 페이지별 추출
            for page_num, text in extract_text_by_page(input_path):
                f.write(f"\n{'='*60}\n")
                f.write(f"PAGE {page_num}\n")
                f.write(f"{'='*60}\n\n")
                f.write(text)
                print(f"  페이지 {page_num}/{total_pages} 추출 완료")

    doc.close()

    file_size = Path(output_path).stat().st_size / 1024
    print("-" * 50)
    print(f"완료: {output_path} ({file_size:.1f}KB)")

    return str(output_path)


def get_pdf_info(pdf_path: str) -> dict:
    """PDF 파일 정보 조회"""
    doc = fitz.open(pdf_path)
    info = {
        "file_path": pdf_path,
        "file_size_mb": Path(pdf_path).stat().st_size / (1024 * 1024),
        "page_count": len(doc),
        "metadata": doc.metadata,
    }
    doc.close()
    return info


def main():
    parser = argparse.ArgumentParser(
        description="PDF 분할 및 텍스트 추출 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf                     # 20페이지씩 분할
  %(prog)s input.pdf -p 10               # 10페이지씩 분할
  %(prog)s input.pdf -o ./output         # 출력 디렉토리 지정
  %(prog)s input.pdf --text              # 텍스트 추출
  %(prog)s input.pdf --text --chunks     # 청크 단위 텍스트 추출
  %(prog)s input.pdf --info              # PDF 정보만 출력
        """
    )

    parser.add_argument("input", help="입력 PDF 파일 경로")
    parser.add_argument("-o", "--output", help="출력 디렉토리 또는 파일 경로")
    parser.add_argument("-p", "--pages", type=int, default=20,
                        help="청크당 페이지 수 (기본: 20)")
    parser.add_argument("--text", action="store_true",
                        help="텍스트 추출 모드 (PDF 분할 대신 텍스트 파일 생성)")
    parser.add_argument("--chunks", action="store_true",
                        help="청크 모드 (--text와 함께 사용)")
    parser.add_argument("--chunk-size", type=int, default=2000,
                        help="청크 크기 (문자 수, 기본: 2000)")
    parser.add_argument("--chunk-overlap", type=int, default=500,
                        help="청크 오버랩 (문자 수, 기본: 500)")
    parser.add_argument("--info", action="store_true",
                        help="PDF 정보만 출력")

    args = parser.parse_args()

    try:
        if args.info:
            # 정보 출력 모드
            info = get_pdf_info(args.input)
            print(f"파일: {info['file_path']}")
            print(f"크기: {info['file_size_mb']:.2f} MB")
            print(f"페이지: {info['page_count']}")
            if info['metadata']:
                print("메타데이터:")
                for key, value in info['metadata'].items():
                    if value:
                        print(f"  {key}: {value}")

            # Claude Code 제한 체크
            print("-" * 50)
            if info['file_size_mb'] > 30:
                print("WARNING: 파일 크기가 30MB를 초과합니다.")
                print("  -> 분할 권장: python pdf_splitter.py input.pdf")
            if info['page_count'] > 100:
                print("WARNING: 페이지 수가 100페이지를 초과합니다.")
                print("  -> 분할 권장: python pdf_splitter.py input.pdf -p 20")
            if info['file_size_mb'] <= 30 and info['page_count'] <= 100:
                print("OK: Claude Code 제한 내에 있습니다.")

        elif args.text:
            # 텍스트 추출 모드
            extract_text_to_file(
                args.input,
                args.output,
                chunk_mode=args.chunks,
                chunk_size=args.chunk_size,
                chunk_overlap=args.chunk_overlap
            )

        else:
            # PDF 분할 모드
            split_pdf(args.input, args.output, args.pages)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
