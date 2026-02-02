#!/usr/bin/env python3
"""PDF에서 이미지 추출 도구"""

import fitz  # PyMuPDF
from pathlib import Path
import sys


def extract_images_from_pdf(pdf_path: Path, output_dir: Path) -> int:
    """PDF에서 모든 이미지를 추출하여 저장

    Args:
        pdf_path: PDF 파일 경로
        output_dir: 이미지 저장 디렉토리

    Returns:
        추출된 이미지 수
    """
    doc = fitz.open(pdf_path)
    pdf_name = pdf_path.stem
    image_count = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]

            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # 파일명: {pdf명}_p{페이지}_{인덱스}.{확장자}
                image_filename = f"{pdf_name}_p{page_num + 1:03d}_{img_index + 1:02d}.{image_ext}"
                image_path = output_dir / image_filename

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                image_count += 1
                print(f"  Extracted: {image_filename}")

            except Exception as e:
                print(f"  Warning: Failed to extract image {img_index} from page {page_num + 1}: {e}")

    doc.close()
    return image_count


def main():
    # 경로 설정
    input_dir = Path(r"C:\claude\ebs\docs\user-manual_split")
    output_dir = Path(r"C:\claude\ebs\docs\user-manual_images")

    # 출력 디렉토리 생성
    output_dir.mkdir(parents=True, exist_ok=True)

    # 모든 PDF 처리
    pdf_files = sorted(input_dir.glob("*.pdf"))
    total_images = 0

    print(f"Found {len(pdf_files)} PDF files")
    print(f"Output directory: {output_dir}\n")

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        count = extract_images_from_pdf(pdf_path, output_dir)
        total_images += count
        print(f"  -> {count} images extracted\n")

    print(f"=" * 50)
    print(f"Total images extracted: {total_images}")
    print(f"Saved to: {output_dir}")


if __name__ == "__main__":
    main()
