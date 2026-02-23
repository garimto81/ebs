#!/usr/bin/env python3
"""
PDF 청크 스크립트 - LLM 입력용 토큰 기반 분할

토큰 수 기반으로 PDF를 청크로 분할하여 JSON으로 출력합니다.
OpenAI tiktoken 또는 간이 토큰 추정 방식 지원.

Usage:
    python pdf_chunker.py input.pdf                     # 기본 4000토큰, JSON 출력
    python pdf_chunker.py input.pdf -t 2000             # 2000토큰씩 분할
    python pdf_chunker.py input.pdf -o chunks.json      # 출력 파일 지정
    python pdf_chunker.py input.pdf --overlap 200       # 오버랩 토큰 지정
    python pdf_chunker.py input.pdf --encoding cl100k   # 토큰 인코딩 지정
"""

import argparse
import io
import json
import re
import sys

# Windows 콘솔 UTF-8 출력 설정
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterator

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF가 설치되지 않았습니다.")
    print("설치: pip install pymupdf")
    sys.exit(1)

# tiktoken은 선택적 의존성
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


@dataclass
class Chunk:
    """청크 데이터 구조"""
    chunk_id: int
    text: str
    token_count: int
    start_page: int
    end_page: int
    char_start: int
    char_end: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ChunkResult:
    """청크 결과 메타데이터"""
    source_file: str
    total_pages: int
    total_chars: int
    total_tokens: int
    chunk_count: int
    max_tokens_per_chunk: int
    overlap_tokens: int
    encoding: str
    chunks: list[Chunk]

    def to_dict(self) -> dict:
        result = asdict(self)
        result['chunks'] = [c.to_dict() for c in self.chunks]
        return result

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class TokenCounter:
    """토큰 카운터 - tiktoken 또는 간이 추정"""

    def __init__(self, encoding: str = "cl100k_base"):
        self.encoding_name = encoding
        self._encoder = None

        if TIKTOKEN_AVAILABLE:
            try:
                self._encoder = tiktoken.get_encoding(encoding)
            except Exception:
                print(f"Warning: '{encoding}' 인코딩 로드 실패, 간이 추정 사용")

    def count(self, text: str) -> int:
        """텍스트의 토큰 수 반환"""
        if self._encoder:
            return len(self._encoder.encode(text))
        else:
            # 간이 추정: 평균 4자 = 1토큰 (영어 기준)
            # 한글의 경우 2-3자 = 1토큰이지만 보수적으로 계산
            return len(text) // 3

    def encode(self, text: str) -> list[int]:
        """텍스트를 토큰 ID 리스트로 변환"""
        if self._encoder:
            return self._encoder.encode(text)
        else:
            # 간이 추정 모드에서는 문자 단위로 처리
            return list(range(len(text)))

    def decode(self, tokens: list[int]) -> str:
        """토큰 ID 리스트를 텍스트로 변환"""
        if self._encoder:
            return self._encoder.decode(tokens)
        else:
            # 간이 추정 모드에서는 지원 안 함
            raise NotImplementedError("간이 추정 모드에서는 decode 미지원")


class PDFChunker:
    """PDF 청크 분할기"""

    def __init__(
        self,
        max_tokens: int = 4000,
        overlap_tokens: int = 200,
        encoding: str = "cl100k_base"
    ):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.counter = TokenCounter(encoding)
        self.encoding = encoding

    def extract_pages(self, pdf_path: str) -> list[tuple[int, str]]:
        """PDF에서 페이지별 텍스트 추출"""
        doc = fitz.open(pdf_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            # 불필요한 공백 정리
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = text.strip()
            pages.append((page_num + 1, text))

        doc.close()
        return pages

    def chunk_text(
        self,
        text: str,
        page_boundaries: list[tuple[int, int, int]]  # (page_num, char_start, char_end)
    ) -> Iterator[Chunk]:
        """
        텍스트를 토큰 기반으로 청크 분할

        Args:
            text: 전체 텍스트
            page_boundaries: 페이지별 문자 위치 정보

        Yields:
            Chunk 객체
        """
        if not text:
            return

        chunk_id = 0
        char_pos = 0
        text_len = len(text)

        while char_pos < text_len:
            # 현재 위치에서 청크 생성
            chunk_text = ""
            chunk_tokens = 0
            chunk_start = char_pos

            # 토큰 제한까지 텍스트 추가
            while char_pos < text_len and chunk_tokens < self.max_tokens:
                # 문장 단위로 추가 시도 (더 자연스러운 분할)
                next_sentence_end = self._find_sentence_end(text, char_pos)

                if next_sentence_end == -1:
                    # 문장 끝을 못 찾으면 나머지 전부
                    next_sentence_end = text_len

                # 다음 문장까지의 텍스트
                next_segment = text[char_pos:next_sentence_end]
                segment_tokens = self.counter.count(next_segment)

                # 토큰 제한 초과 체크
                if chunk_tokens + segment_tokens > self.max_tokens and chunk_text:
                    break

                chunk_text += next_segment
                chunk_tokens += segment_tokens
                char_pos = next_sentence_end

            if not chunk_text.strip():
                break

            # 페이지 범위 계산
            start_page, end_page = self._get_page_range(
                chunk_start, char_pos, page_boundaries
            )

            chunk = Chunk(
                chunk_id=chunk_id,
                text=chunk_text.strip(),
                token_count=chunk_tokens,
                start_page=start_page,
                end_page=end_page,
                char_start=chunk_start,
                char_end=char_pos
            )

            yield chunk
            chunk_id += 1

            # 오버랩 처리: 이전 청크 끝부분부터 다시 시작
            if self.overlap_tokens > 0 and char_pos < text_len:
                overlap_chars = self._estimate_chars_for_tokens(
                    chunk_text, self.overlap_tokens
                )
                char_pos = max(chunk_start + 1, char_pos - overlap_chars)

    def _find_sentence_end(self, text: str, start: int) -> int:
        """다음 문장 끝 위치 찾기"""
        # 문장 종결 패턴
        patterns = ['. ', '.\n', '? ', '?\n', '! ', '!\n', '.\t', '。', '\n\n']

        min_pos = -1
        for pattern in patterns:
            pos = text.find(pattern, start)
            if pos != -1:
                # 패턴 끝 위치 반환
                end_pos = pos + len(pattern)
                if min_pos == -1 or end_pos < min_pos:
                    min_pos = end_pos

        # 문장 끝을 못 찾았지만 500자 이상이면 단어 경계에서 자르기
        if min_pos == -1 and len(text) - start > 500:
            space_pos = text.find(' ', start + 500)
            if space_pos != -1:
                return space_pos + 1

        return min_pos

    def _get_page_range(
        self,
        char_start: int,
        char_end: int,
        page_boundaries: list[tuple[int, int, int]]
    ) -> tuple[int, int]:
        """문자 위치에서 페이지 범위 계산"""
        start_page = 1
        end_page = 1

        for page_num, p_start, p_end in page_boundaries:
            if p_start <= char_start < p_end:
                start_page = page_num
            if p_start < char_end <= p_end:
                end_page = page_num

        return start_page, end_page

    def _estimate_chars_for_tokens(self, text: str, target_tokens: int) -> int:
        """특정 토큰 수에 해당하는 대략적인 문자 수 추정"""
        total_tokens = self.counter.count(text)
        if total_tokens == 0:
            return 0

        chars_per_token = len(text) / total_tokens
        return int(target_tokens * chars_per_token)

    def process(self, pdf_path: str) -> ChunkResult:
        """PDF 파일을 청크로 분할"""
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")

        # 페이지별 텍스트 추출
        pages = self.extract_pages(pdf_path)

        # 전체 텍스트 조합 및 페이지 경계 기록
        full_text = ""
        page_boundaries = []

        for page_num, text in pages:
            start = len(full_text)
            full_text += text + "\n\n"
            end = len(full_text)
            page_boundaries.append((page_num, start, end))

        # 토큰 기반 청크 분할
        chunks = list(self.chunk_text(full_text, page_boundaries))

        total_tokens = self.counter.count(full_text)

        return ChunkResult(
            source_file=str(path.absolute()),
            total_pages=len(pages),
            total_chars=len(full_text),
            total_tokens=total_tokens,
            chunk_count=len(chunks),
            max_tokens_per_chunk=self.max_tokens,
            overlap_tokens=self.overlap_tokens,
            encoding=self.encoding if TIKTOKEN_AVAILABLE else "estimate",
            chunks=chunks
        )


def main():
    parser = argparse.ArgumentParser(
        description="PDF 청크 스크립트 - LLM 입력용 토큰 기반 분할",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.pdf                      # 기본 4000토큰, JSON 출력
  %(prog)s input.pdf -t 2000              # 2000토큰씩 분할
  %(prog)s input.pdf -o chunks.json       # 출력 파일 지정
  %(prog)s input.pdf --overlap 200        # 오버랩 토큰 지정
  %(prog)s input.pdf --encoding cl100k    # 토큰 인코딩 지정 (tiktoken)
  %(prog)s input.pdf --info               # PDF 정보만 출력
  %(prog)s input.pdf --preview 3          # 처음 3개 청크 미리보기
        """
    )

    parser.add_argument("input", help="입력 PDF 파일 경로")
    parser.add_argument("-o", "--output", help="출력 JSON 파일 경로")
    parser.add_argument("-t", "--tokens", type=int, default=4000,
                        help="청크당 최대 토큰 수 (기본: 4000)")
    parser.add_argument("--overlap", type=int, default=200,
                        help="청크 간 오버랩 토큰 수 (기본: 200)")
    parser.add_argument("--encoding", default="cl100k_base",
                        help="tiktoken 인코딩 (기본: cl100k_base)")
    parser.add_argument("--info", action="store_true",
                        help="PDF 정보만 출력")
    parser.add_argument("--preview", type=int, metavar="N",
                        help="처음 N개 청크 미리보기 (텍스트 일부 표시)")
    parser.add_argument("--quiet", action="store_true",
                        help="진행 메시지 숨기기")
    parser.add_argument('--prd', action='store_true', help='PRD 전용 계층형 청킹 활성화')
    parser.add_argument('--strategy', choices=['auto', 'fixed', 'hierarchical', 'semantic'], default='auto', help='청킹 전략 (--prd 활성화 시)')
    parser.add_argument('--threshold', type=int, default=60000, help='청킹 임계 토큰 수 (기본: 60000)')

    args = parser.parse_args()

    # MD 파일 처리 분기 (기존 PDF 경로 앞에 삽입)
    if Path(args.input).suffix.lower() in ('.md', '.markdown'):
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'lib' / '..'))
        from lib.pdf_utils.md_chunker import MDChunker
        max_tok = 8000 if args.prd else args.tokens
        overlap = 400 if args.prd else args.overlap
        chunker_md = MDChunker(
            strategy=args.strategy if args.prd else 'fixed',
            max_tokens=max_tok,
            overlap=overlap,
            threshold=args.threshold,
        )
        result_md = chunker_md.process(args.input)
        import json as _json
        out = result_md.to_dict()
        if args.output:
            Path(args.output).write_text(_json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"청킹 완료: {args.input}")
            print(f"- 청크 수: {result_md.chunk_count}개")
            print(f"- 총 토큰: {result_md.total_tokens:,}")
            print(f"- 전략: {result_md.strategy}")
            print(f"- 출력 파일: {args.output}")
        else:
            print(_json.dumps(out, ensure_ascii=False, indent=2))
        return  # PDF 처리 경로로 가지 않도록 조기 반환

    try:
        chunker = PDFChunker(
            max_tokens=args.tokens,
            overlap_tokens=args.overlap,
            encoding=args.encoding
        )

        if args.info:
            # PDF 정보만 출력
            doc = fitz.open(args.input)
            file_size = Path(args.input).stat().st_size / (1024 * 1024)

            print(f"파일: {args.input}")
            print(f"크기: {file_size:.2f} MB")
            print(f"페이지: {len(doc)}")

            # 토큰 추정
            total_text = ""
            for page in doc:
                total_text += page.get_text()
            doc.close()

            token_count = chunker.counter.count(total_text)
            estimated_chunks = (token_count + args.tokens - 1) // args.tokens

            print(f"문자 수: {len(total_text):,}")
            print(f"추정 토큰: {token_count:,}")
            print(f"예상 청크 수: {estimated_chunks} ({args.tokens}토큰 기준)")

            if not TIKTOKEN_AVAILABLE:
                print("\nNote: tiktoken 미설치, 토큰 수는 추정값입니다.")
                print("정확한 계산: pip install tiktoken")

            return

        if not args.quiet:
            print(f"처리 중: {args.input}")
            print(f"설정: {args.tokens}토큰/청크, {args.overlap}토큰 오버랩")
            if not TIKTOKEN_AVAILABLE:
                print("Note: tiktoken 미설치, 간이 토큰 추정 사용")

        # 청크 분할
        result = chunker.process(args.input)

        if not args.quiet:
            print(f"완료: {result.chunk_count}개 청크 생성")
            print(f"총 토큰: {result.total_tokens:,}")

        # 미리보기 모드
        if args.preview:
            print("\n" + "=" * 60)
            print(f"청크 미리보기 (처음 {args.preview}개)")
            print("=" * 60)

            for chunk in result.chunks[:args.preview]:
                preview_text = chunk.text[:200] + "..." if len(chunk.text) > 200 else chunk.text
                print(f"\n[Chunk {chunk.chunk_id}] 페이지 {chunk.start_page}-{chunk.end_page}, {chunk.token_count}토큰")
                print("-" * 40)
                print(preview_text)

            print("\n" + "=" * 60)

        # JSON 출력
        json_output = result.to_json()

        if args.output:
            output_path = Path(args.output)
        else:
            # 출력 파일 미지정 시 자동 생성
            input_path = Path(args.input)
            output_path = input_path.with_suffix(".chunks.json")

        # JSON 저장 (UTF-8 BOM 없이)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_output)

        if not args.quiet:
            print(f"저장됨: {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
