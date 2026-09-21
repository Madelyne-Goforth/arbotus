#!/usr/bin/env bash
# Run from the arbotus repo root, venv active. Fill in each --url below
# with the exact armypubs.army.mil link you downloaded that PDF from
# (check your browser history/downloads if you don't remember).
set -e

python3 src/main.py ingest docs_raw/adp_1.txt \
  --doc-id ADP1 --title "The Army" \
  --url "https://armypubs.army.mil/ProductMaps/PubForm/Details.aspx?PUB_ID=1007346"

python3 src/main.py ingest docs_raw/adp_2-0.txt \
  --doc-id ADP2-0 --title "Intelligence" \
  --url "https://armypubs.army.mil/ProductMaps/PubForm/Details.aspx?PUB_ID=1007351"

python3 src/main.py ingest docs_raw/adp_3-0.txt \
  --doc-id ADP3-0 --title "Operations" \
  --url "https://armypubs.army.mil/ProductMaps/PubForm/Details.aspx?PUB_ID=1030747"

python3 src/main.py ingest docs_raw/adp_6-22.txt \
  --doc-id ADP6-22 --title "Army Leadership and the Profession" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN42975-ADP_6-22-002-WEB-8.pdf"

python3 src/main.py ingest docs_raw/ar_25-2.txt \
  --doc-id AR25-2 --title "Army Cybersecurity" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN37506-AR_25-2-003-WEB-4.pdf"

python3 src/main.py ingest docs_raw/ar_600-25.txt \
  --doc-id AR600-25 --title "Salutes, Honors, and Visits of Courtesy" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN44891-AR_600-25-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/ar_670-1.txt \
  --doc-id AR670-1 --title "Wear and Appearance of Army Uniforms and Insignia" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN30964-AR_670-1-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/atp_3-21-8.txt \
  --doc-id ATP3-21.8 --title "Infantry Platoon and Squad" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN44065-ATP_3-21.8-001-WEB-3.pdf"

python3 src/main.py ingest docs_raw/atp_3-34-40.txt \
  --doc-id ATP3-34.40 --title "General Engineering" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN37985-ATP_3-34.40-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/atp_4-90.txt \
  --doc-id ATP4-90 --title "Brigade Support Battalion" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN45712-ATP_4-90-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/fm_2-0.txt \
  --doc-id FM2-0 --title "Intelligence" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN39259-FM_2-0-000-WEB-2.pdf"

python3 src/main.py ingest docs_raw/fm_3-12.txt \
  --doc-id FM3-12 --title "Cyberspace Operations and Electromagnetic Warfare" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN3089_FM%203-12%20FINAL%20WEB%201.pdf"

python3 src/main.py ingest docs_raw/fm_3-34.txt \
  --doc-id FM3-34 --title "Engineer Operations" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN45471-FM_3-34-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/fm_4-0.txt \
  --doc-id FM4-0 --title "Sustainment Operations" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN46157-FM_4-0-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/tc_3-21-5.txt \
  --doc-id TC3-21.5 --title "Drill and Ceremonies" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN32297-TC_3-21.5-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/tc_3-21-76.txt \
  --doc-id TC3-21.76 --title "Ranger Handbook" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN45113-TC_3-21.76-000-WEB-2.pdf"

python3 src/main.py ingest docs_raw/atp_3-09-30.txt \
  --doc-id ATP3-09.30 --title "Observed Fires" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN5011_ATP%203-09x30%20FINAL%20WEB.pdf"

python3 src/main.py ingest docs_raw/atp_3-12-3.txt \
  --doc-id ATP3-12.3 --title "Electromagnetic Warfare Techniques" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN44803-ATP_3-12.3-002-WEB-3.pdf"

python3 src/main.py ingest docs_raw/tc_3-22-50.txt \
  --doc-id TC3-22.50 --title "Heavy Machine Gun, M2 Series" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN5846_TC%203-22x50%20FINAL%20WEB.pdf"

python3 src/main.py ingest docs_raw/tc_3-22-240.txt \
  --doc-id TC3-22.240 --title "Medium Machine Gun, M240 Series" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN3182-TC_3-22.240-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/tc_3-22-249.txt \
  --doc-id TC3-22.249 --title "Light Machine Gun, M249 Series" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN3242-TC_3-22.249-000-WEB-1.pdf"

python3 src/main.py ingest docs_raw/tc_3-22-9.txt \
  --doc-id TC3-22.9 --title "Rifle and Carbine" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/pdf/web/ARN19927_TC_3-22x9_C3_FINAL_WEB.pdf"

echo "All 22 ingested."
