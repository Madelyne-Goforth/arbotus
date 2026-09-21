import argparse
import sys
from pathlib import Path

from pdf2image import convert_from_path
import pytesseract


def ocr_text(pdf_path: Path, dpi: int = 300) -> str:
    pages_text = []
    images = convert_from_path(str(pdf_path), dpi=dpi)
    for i, image in enumerate(images, start=1):
        print(f"  OCR'ing page {i}/{len(images)}...", file=sys.stderr)
        page_text = pytesseract.image_to_string(image)
        pages_text.append(page_text)
    return "\n\n".join(pages_text)


def main():
    parser = argparse.ArgumentParser(
        description="OCR-based PDF text extraction, for PDFs with a broken/missing text layer "
                    "(pdf_to_text.py fails or produces (cid:N) garbage on these)."
    )
    parser.add_argument("pdf_file", help="path to the source PDF")
    parser.add_argument("output_file", help="path to write the extracted .txt to")
    parser.add_argument("--dpi", type=int, default=300, help="render resolution before OCR (default 300)")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    text = ocr_text(pdf_path, dpi=args.dpi)

    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text)

    print(f"OCR'd {len(text)} characters from {pdf_path.name} -> {output_path}")
    print("OCR is lower-fidelity than a real text layer -- specifically check that paragraph-number "
          "headers (e.g. '3-4.') came through correctly, since chunker.py's section regex depends on them.")


if __name__ == "__main__":
    main()