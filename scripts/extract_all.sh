#!/usr/bin/env bash
# Run this from the arbotus repo root, venv active.
set -e
SRC=~/Desktop/"Army Pubs"

python3 scripts/pdf_to_text.py "$SRC/ADP_1.pdf"        docs_raw/adp_1.txt
python3 scripts/pdf_to_text.py "$SRC/ADP_2-0.pdf"      docs_raw/adp_2-0.txt
python3 scripts/pdf_to_text.py "$SRC/ADP_3-0.pdf"      docs_raw/adp_3-0.txt
python3 scripts/pdf_to_text.py "$SRC/ADP_6-22.pdf"     docs_raw/adp_6-22.txt
python3 scripts/pdf_to_text.py "$SRC/AR_25-2.pdf"      docs_raw/ar_25-2.txt
python3 scripts/pdf_to_text.py "$SRC/AR_600-25.pdf"    docs_raw/ar_600-25.txt
python3 scripts/pdf_to_text.py "$SRC/AR_670-1.pdf"     docs_raw/ar_670-1.txt
python3 scripts/pdf_to_text.py "$SRC/ATP_3-21.8.pdf"   docs_raw/atp_3-21-8.txt
python3 scripts/pdf_to_text.py "$SRC/ATP_3-34.40.pdf"  docs_raw/atp_3-34-40.txt
python3 scripts/pdf_to_text.py "$SRC/ATP_4-90.pdf"     docs_raw/atp_4-90.txt
python3 scripts/pdf_to_text.py "$SRC/FM_2-0.pdf"       docs_raw/fm_2-0.txt
python3 scripts/pdf_to_text.py "$SRC/FM_3-12.pdf"      docs_raw/fm_3-12.txt
python3 scripts/pdf_to_text.py "$SRC/FM_3-34.pdf"      docs_raw/fm_3-34.txt
python3 scripts/pdf_to_text.py "$SRC/FM_4-0.pdf"       docs_raw/fm_4-0.txt
python3 scripts/pdf_to_text.py "$SRC/TC_3-21.5.pdf"    docs_raw/tc_3-21-5.txt
python3 scripts/pdf_to_text.py "$SRC/TC_3-21.76.pdf"   docs_raw/tc_3-21-76.txt
python3 scripts/pdf_to_text.py "$SRC/ATP 3-09.pdf"     docs_raw/atp_3-09-30.txt
python3 scripts/pdf_to_text.py "$SRC/ATP_3-12.3.pdf"   docs_raw/atp_3-12-3.txt
python3 scripts/pdf_to_text.py "$SRC/TC 3-22.pdf"      docs_raw/tc_3-22-50.txt
python3 scripts/pdf_to_text.py "$SRC/TC_3-22.240.pdf"  docs_raw/tc_3-22-240.txt
python3 scripts/pdf_to_text.py "$SRC/TC_3-22.249.pdf"  docs_raw/tc_3-22-249.txt
python3 scripts/pdf_to_text.py "$SRC/TC_3-22.9.pdf"    docs_raw/tc_3-22-9.txt

echo "All extracted. Skim docs_raw/*.txt before ingesting any of them."
