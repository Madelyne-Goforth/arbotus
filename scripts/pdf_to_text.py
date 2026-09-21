"""
Extracts plain text from a doctrine PDF into a .txt file under docs_raw/,
ready for main.py's `ingest` command.

Uses the poppler `pdftotext` command-line tool (via subprocess), not
pdfplumber. Switched from pdfplumber because pdfplumber's font-encoding
handling produced (cid:N) glyph-ID garbage on most of AR-BOTUS's real
doctrine PDFs; pdftotext handled the same files cleanly. Two PDFs
(ADP 1, ADP 2-0) are broken under both tools (missing/corrupt embedded
font encoding) -- those go through scripts/ocr_pdf_to_text.py instead.

Requires poppler installed on whatever machine runs this:
    macOS:  brew install poppler
    Debian/Raspberry Pi OS:  sudo apt install poppler-utils

This does NOT try to detect or fix broken paragraph-header formatting --
PDF text extraction can split words oddly across line breaks, drop
section numbers that were rendered as images, etc. Always skim the
output before ingesting it; chunker.py's SECTION_HEADER_RE only finds
paragraphs whose "3-4." style header survived extraction cleanly.

Usage:
    python3 scripts/pdf_to_text.py path/to/source.pdf docs_raw/output.txt
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def extract_text(pdf_path: Path) -> str:
    # Input: pdf_path -- a pathlib.Path to the source PDF
    # Output: the PDF's text via pdftotext, all pages concatenated
    # Use case: called once by main() below, before writing to disk.
    result = subprocess.run(
        ["pdftotext", str(pdf_path), "-"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description="Extract PDF text for AR-BOTUS ingestion")
    parser.add_argument("pdf_file", help="path to the source PDF")
    parser.add_argument("output_file", help="path to write the extracted .txt to")
    args = parser.parse_args()

    if shutil.which("pdftotext") is None:
        print("pdftotext not found. Install poppler:")
        print("  macOS:  brew install poppler")
        print("  Debian/Raspberry Pi OS:  sudo apt install poppler-utils")
        sys.exit(1)

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
