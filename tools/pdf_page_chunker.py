#!/usr/bin/env python3
"""
PDF 페이지 기반 청킹 스크립트 - 레이아웃 100% 보존

PDF를 페이지 단위로 분할하여 텍스트 + 이미지 레이아웃을 완벽하게 보존합니다.
멀티모달 LLM에 직접 전달 가능한 형태로 출력합니다.

출력 형식:
- file: 분할된 PDF 파일들 (기본)
- inline: Base64 인코딩된 JSON (API 전송용)

Usage:
    python pdf_page_chunker.py input.pdf                     # 기본 10페이지씩 분할
    python pdf_page_chunker.py input.pdf --pages 20          # 20페이지씩 분할
    python pdf_page_chunker.py input.pdf --format inline     # Base64 JSON 출력
    python pdf_page_chunker.py input.pdf --info              # PDF 정보만 출력
"""

import argparse
import base64
import io
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# Windows 콘솔 UTF-8 출력 설정
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF가 설치되지 않았습니다.")
    print("설치: pip install pymupdf")
    sys.exit(1)


@dataclass
class PageChunk:
    """페이지 기반 청크 데이터"""
    chunk_id: int
    start_page: int
    end_page: int
    page_count: int
    file_path: str | None = None  # file 모드
    data_base64: str | None = None  # inline 모드
    media_type: str = "application/pdf"

    def to_dict(self) -> dict:
        result = asdict(self)
        # None 값 제거
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class PageChunkResult:
    """페이지 기반 청크 결과"""
    source_file: str
    total_pages: int
    pages_per_chunk: int
    chunk_count: int
    format: str  # "file" or "inline"
    output_dir: str | None = None  # file 모드
    chunks: list[PageChunk] = None

    def __post_init__(self):
        if self.chunks is None:
            self.chunks = []

    def to_dict(self) -> dict:
        result = {
            "source_file": self.source_file,
            "total_pages": self.total_pages,
            "pages_per_chunk": self.pages_per_chunk,
            "chunk_count": self.chunk_count,
            "format": self.format,
            "chunks": [c.to_dict() for c in self.chunks]
        }
        if self.output_dir:
            result["output_dir"] = self.output_dir
        return result

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class PDFPageChunker:
    """PDF 페이지 기반 분할기 - 레이아웃 100% 보존"""

    def __init__(self, pages_per_chunk: int = 10):
        """
        Args:
            pages_per_chunk: 청크당 페이지 수 (기본: 10)
        """
        self.pages_per_chunk = pages_per_chunk

    def get_info(self, pdf_path: str) -> dict:
        """PDF 정보 반환"""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")

        doc = fitz.open(pdf_path)
        file_size_mb = path.stat().st_size / (1024 * 1024)

        # 메타데이터 추출
        metadata = doc.metadata

        # 텍스트 및 이미지 정보
        total_chars = 0
        total_images = 0

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            total_chars += len(page.get_text())
            total_images += len(page.get_images())

        estimated_chunks = (len(doc) + self.pages_per_chunk - 1) // self.pages_per_chunk

        info = {
            "file_path": str(path.absolute()),
            "file_size_mb": round(file_size_mb, 2),
            "total_pages": len(doc),
            "total_chars": total_chars,
            "total_images": total_images,
            "estimated_chunks": estimated_chunks,
            "pages_per_chunk": self.pages_per_chunk,
            "metadata": {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
            }
        }

        doc.close()
        return info

    def split_to_files(self, pdf_path: str, output_dir: str | None = None) -> PageChunkResult:
        """
        PDF를 분할 파일로 출력

        Args:
            pdf_path: 입력 PDF 경로
            output_dir: 출력 디렉토리 (기본: <입력파일명>_split/)

        Returns:
            PageChunkResult with file paths
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")

        # 출력 디렉토리 설정
        if output_dir:
            out_dir = Path(output_dir)
        else:
            out_dir = path.parent / f"{path.stem}_split"

        out_dir.mkdir(parents=True, exist_ok=True)

        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        chunks = []
        chunk_id = 0

        for start_idx in range(0, total_pages, self.pages_per_chunk):
            end_idx = min(start_idx + self.pages_per_chunk, total_pages)

            # 1-indexed 페이지 번호
            start_page = start_idx + 1
            end_page = end_idx

            # 새 PDF 문서 생성
            new_doc = fitz.open()

            # 페이지 복사 (레이아웃 100% 보존)
            new_doc.insert_pdf(doc, from_page=start_idx, to_page=end_idx - 1)

            # 파일명 생성 (001-010 형식)
            chunk_filename = f"{path.stem}_p{start_page:03d}-{end_page:03d}.pdf"
            chunk_path = out_dir / chunk_filename

            # 저장
            new_doc.save(str(chunk_path))
            new_doc.close()

            chunk = PageChunk(
                chunk_id=chunk_id,
                start_page=start_page,
                end_page=end_page,
                page_count=end_idx - start_idx,
                file_path=str(chunk_path.absolute())
            )
            chunks.append(chunk)
            chunk_id += 1

        doc.close()

        return PageChunkResult(
            source_file=str(path.absolute()),
            total_pages=total_pages,
            pages_per_chunk=self.pages_per_chunk,
            chunk_count=len(chunks),
            format="file",
            output_dir=str(out_dir.absolute()),
            chunks=chunks
        )

    def split_to_inline(self, pdf_path: str) -> PageChunkResult:
        """
        PDF를 Base64 인코딩된 청크로 변환 (API 전송용)

        Args:
            pdf_path: 입력 PDF 경로

        Returns:
            PageChunkResult with base64 data
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")

        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        chunks = []
        chunk_id = 0

        for start_idx in range(0, total_pages, self.pages_per_chunk):
            end_idx = min(start_idx + self.pages_per_chunk, total_pages)

            start_page = start_idx + 1
            end_page = end_idx

            # 새 PDF 문서 생성
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start_idx, to_page=end_idx - 1)

            # 메모리에 PDF 바이트로 저장
            pdf_bytes = new_doc.tobytes()
            new_doc.close()

            # Base64 인코딩
            b64_data = base64.b64encode(pdf_bytes).decode('utf-8')

            chunk = PageChunk(
                chunk_id=chunk_id,
                start_page=start_page,
                end_page=end_page,
                page_count=end_idx - start_idx,
                data_base64=b64_data,
                media_type="application/pdf"
            )
            chunks.append(chunk)
            chunk_id += 1

        doc.close()

        return PageChunkResult(
            source_file=str(path.absolute()),
            total_pages=total_pages,
            pages_per_chunk=self.pages_per_chunk,
            chunk_count=len(chunks),
            format="inline",
            chunks=chunks
        )

    def process(self, pdf_path: str, format: str = "file", output_dir: str | None = None) -> PageChunkResult:
        """
        PDF 분할 (통합 인터페이스)

        Args:
            pdf_path: 입력 PDF 경로
            format: "file" 또는 "inline"
            output_dir: 출력 디렉토리 (file 모드 전용)

        Returns:
            PageChunkResult
        """
        if format == "inline":
            return self.split_to_inline(pdf_path)
        else:
            return self.split_to_files(pdf_path, output_dir)


def print_info(info: dict) -> None:
    """PDF 정보 출력"""
    print(f"파일: {info['file_path']}")
    print(f"크기: {info['file_size_mb']:.2f} MB")
    print(f"페이지: {info['total_pages']}")
    print(f"문자 수: {info['total_chars']:,}")
    print(f"이미지 수: {info['total_images']}")
    print(f"예상 청크 수: {info['estimated_chunks']} ({info['pages_per_chunk']}페이지 기준)")

    # 메타데이터
    meta = info['metadata']
    if meta.get('title'):
        print(f"제목: {meta['title']}")
    if meta.get('author'):
        print(f"저자: {meta['author']}")


def main():
    parser = argparse.ArgumentParser(
        description="PDF 페이지 기반 청킹 - 레이아웃 100%% 보존",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf_page_chunker.py input.pdf                      # 기본 10페이지씩 분할
  pdf_page_chunker.py input.pdf --pages 20           # 20페이지씩 분할
  pdf_page_chunker.py input.pdf --format inline      # Base64 JSON 출력
  pdf_page_chunker.py input.pdf --info               # PDF 정보만 출력
  pdf_page_chunker.py input.pdf -o ./output          # 출력 디렉토리 지정

토큰 기반 청킹 vs 페이지 기반 청킹:
  - 토큰 기반 (pdf_chunker.py): 텍스트만 추출, 이미지 손실
  - 페이지 기반 (이 스크립트): PDF 자체 분할, 레이아웃 100%% 보존
        """
    )

    parser.add_argument("input", help="입력 PDF 파일 경로")
    parser.add_argument("--pages", type=int, default=10,
                        help="청크당 페이지 수 (기본: 10)")
    parser.add_argument("--format", choices=["file", "inline"], default="file",
                        help="출력 형식: file (분할 PDF) 또는 inline (Base64 JSON)")
    parser.add_argument("-o", "--output", help="출력 경로 (file: 디렉토리, inline: JSON 파일)")
    parser.add_argument("--info", action="store_true",
                        help="PDF 정보만 출력")
    parser.add_argument("--quiet", action="store_true",
                        help="진행 메시지 숨기기")

    args = parser.parse_args()

    try:
        chunker = PDFPageChunker(pages_per_chunk=args.pages)

        # 정보 모드
        if args.info:
            info = chunker.get_info(args.input)
            print_info(info)
            return

        if not args.quiet:
            print(f"처리 중: {args.input}")
            print(f"설정: {args.pages}페이지/청크, {args.format} 모드")

        # 분할 실행
        if args.format == "file":
            result = chunker.split_to_files(args.input, args.output)

            if not args.quiet:
                print(f"완료: {result.chunk_count}개 청크 생성")
                print(f"출력 디렉토리: {result.output_dir}")
                print("\n생성된 파일:")
                for chunk in result.chunks:
                    print(f"  - {Path(chunk.file_path).name} (p{chunk.start_page}-{chunk.end_page})")

            # 메타데이터 JSON도 저장
            meta_path = Path(result.output_dir) / "chunks_meta.json"
            with open(meta_path, "w", encoding="utf-8") as f:
                f.write(result.to_json())

            if not args.quiet:
                print(f"\n메타데이터: {meta_path}")

        else:  # inline 모드
            result = chunker.split_to_inline(args.input)
            json_output = result.to_json()

            if args.output:
                output_path = Path(args.output)
            else:
                input_path = Path(args.input)
                output_path = input_path.with_suffix(".page_chunks.json")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_output)

            if not args.quiet:
                print(f"완료: {result.chunk_count}개 청크 생성")
                print(f"저장됨: {output_path}")

                # Base64 크기 정보
                total_b64_size = sum(len(c.data_base64) for c in result.chunks if c.data_base64)
                print(f"총 Base64 크기: {total_b64_size / (1024*1024):.2f} MB")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
