"""
Extracts plain text from a doctrine PDF into a .txt file under docs_raw/,
ready for main.py's `ingest` command.

Uses pdfplumber (pure Python, no system-level poppler/pdftotext install
needed -- matters for eventually running this on the Pi too).

This does NOT try to detect or fix broken paragraph-header formatting --
PDF text extraction can split words oddly across line breaks, drop
section numbers that were rendered as images, etc. Always skim the
output before ingesting it; chunker.py's SECTION_HEADER_RE only finds
paragraphs whose "3-4." style header survived extraction cleanly.

Usage:
    python3 scripts/pdf_to_text.py path/to/source.pdf docs_raw/output.txt
"""

import argparse
import sys
from pathlib import Path

import pdfplumber


def extract_text(pdf_path: Path) -> str:
    # Input: pdf_path -- a pathlib.Path to the source PDF
    # Output: the PDF's text, all pages concatenated, pages separated by
    #         a blank line (so a section that got split across a page
    #         break still has clear whitespace around it)
    # Use case: called once by main() below, before writing to disk.
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            pages_text.append(page_text)
    return "\n\n".join(pages_text)


def main():
    parser = argparse.ArgumentParser(description="Extract PDF text for AR-BOTUS ingestion")
    parser.add_argument("pdf_file", help="path to the source PDF")
    parser.add_argument("output_file", help="path to write the extracted .txt to")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    text = extract_text(pdf_path)

    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text)

    print(f"Extracted {len(text)} characters from {pdf_path.name} -> {output_path}")
    print("Skim the output before ingesting -- PDF extraction can mangle section headers.")


if __name__ == "__main__":
    main()
