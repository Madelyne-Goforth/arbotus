# AR-BOTUS

**Offline, local RAG-based mentor over Army doctrine.**

Ask a question, it retrieves the relevant doctrine excerpts (tagged with
document, section, source URL, and pull date), then a locally-run LLM
comments on them in a senior-mentor persona. Retrieved doctrine and AI
commentary are kept structurally separate in the output -- the *code*
guarantees this split, not a prompt instruction the model could ignore.

Runs fully offline via [Ollama](https://ollama.com) -- no cloud API, no
network dependency once set up. Built to eventually run on a Raspberry
Pi 5; currently developed and tested on macOS.

## Architecture

```
Army Pubs/*.pdf --> pdf_to_text.py / ocr_pdf_to_text.py --> docs_raw/*.txt
                                                                  |
                                                                  v
                                                            chunker.py
                                                                  |
                                                                  v
                                                Chunk objects (schema.py)
                                                                  |
                                                                  v
                                              vectorstore.py (Chroma, on-disk)
                                                                  |
                                          question --> query --> top-k chunks
                                                                  |
                                                                  v
                                                            mentor.py
                                        (renders retrieved block deterministically,
                                         then calls Ollama for mentor commentary)
                                                                  |
                                                   -------------------------------
                                                   |                             |
                                              src/main.py                   src/app.py
                                            (terminal CLI)              (local web GUI, Flask)
```

Both the CLI and the web GUI are thin callers of the same `mentor.ask()`
-- neither has its own copy of the retrieval/generation logic.

## Setup

```bash
git clone <this repo>
cd arbotus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# install Ollama if you haven't: https://ollama.com/download
ollama pull nomic-embed-text     # embedding model
ollama pull llama3.2:3b          # generation model
```

The doctrine text is already committed under `docs_raw/` -- ingest it
once (see below) and you're ready to ask questions.

## Usage

### Web GUI (recommended)

```bash
./run.sh
```

Opens `http://localhost:5000` automatically -- a two-pane chat interface,
retrieved doctrine on one side, mentor commentary on the other, fully
offline.

### Terminal / CLI

```bash
python3 src/main.py check        # confirms Ollama is reachable

# one-time: ingest the full doctrine set (see Doctrine library below)
./scripts/ingest_all.sh

python3 src/main.py ask "what's the fingernail standard for females"
```

## Doctrine library

22 U.S. Army doctrine publications, focused on Army ROTC fundamentals
(appearance, drill, Ranger Challenge events, tactics) with some broader
Army-wide context. All public release, unclassified, sourced from
[armypubs.army.mil](https://armypubs.army.mil).

| Doc ID | Title |
|---|---|
| ADP 1 | The Army |
| ADP 2-0 | Intelligence |
| ADP 3-0 | Operations |
| ADP 6-22 | Army Leadership and the Profession |
| AR 25-2 | Army Cybersecurity |
| AR 600-25 | Salutes, Honors, and Visits of Courtesy |
| AR 670-1 | Wear and Appearance of Army Uniforms and Insignia |
| ATP 3-09.30 | Observed Fires |
| ATP 3-12.3 | Electromagnetic Warfare Techniques |
| ATP 3-21.8 | Infantry Platoon and Squad |
| ATP 3-34.40 | General Engineering |
| ATP 4-90 | Brigade Support Battalion |
| FM 2-0 | Intelligence |
| FM 3-12 | Cyberspace Operations and Electromagnetic Warfare |
| FM 3-34 | Engineer Operations |
| FM 4-0 | Sustainment Operations |
| TC 3-21.5 | Drill and Ceremonies |
| TC 3-21.76 | Ranger Handbook |
| TC 3-22.9 | Rifle and Carbine |
| TC 3-22.50 | Heavy Machine Gun, M2 Series |
| TC 3-22.240 | Medium Machine Gun, M240 Series |
| TC 3-22.249 | Light Machine Gun, M249 Series |

**Scope note:** no joint (JP-series) publications are included, even
where they'd be relevant background. Joint pubs are commonly
CAC/DoD-network-gated, and this repo is public -- not worth the
distribution risk even for publicly releasable content.

### Adding more doctrine

1. Pull a doctrine PDF from [armypubs.army.mil](https://armypubs.army.mil)
   into a local `Army Pubs/` folder (sibling to this repo, not committed).
2. Extract it:
   ```bash
   python scripts/pdf_to_text.py "../Army Pubs/YOUR_DOC.pdf" docs_raw/your_doc.txt
   ```
   If the output has `(cid:` garbage in it, the PDF has a broken font
   encoding -- fall back to OCR instead:
   ```bash
   python scripts/ocr_pdf_to_text.py "../Army Pubs/YOUR_DOC.pdf" docs_raw/your_doc.txt
   ```
3. Add an entry to `scripts/extract_all.sh` and `scripts/ingest_all.sh`
   (doc ID, title, and the real source URL), then re-run
   `./scripts/ingest_all.sh`.

The chunker splits on Army paragraph-header style (`3-4.` or the AR-series
en-dash form `3–4.`) via the pattern in `chunker.py`. It's been hardened
against the real-world extraction issues found while building this
library: OCR misreading `.` as `,`, back-of-index cross-reference lines
that look like headers, and long unheadered stretches (tables/appendices)
that would otherwise balloon into oversized chunks.

## Design principles

- **Retrieval is ground truth, generation is commentary.** The mentor
  persona (`MENTOR_SYSTEM_PROMPT` in `mentor.py`) is explicitly
  instructed to never contradict retrieved doctrine, never invent a
  citation, and say so plainly when nothing relevant was retrieved --
  rather than fall back on the model's own general knowledge.
- **Structural, not instructional, separation.** `format_retrieved_block()`
  renders retrieved excerpts by deterministic code before the LLM ever
  runs. The model is never trusted to self-report which parts of its
  output are verbatim doctrine vs. its own synthesis.
- **Fully offline.** No cloud API calls anywhere in the pipeline --
  embeddings and generation both run locally via Ollama.
- **Extraction failures fail loud, not silent.** Chunking and ingestion
  guard against duplicate IDs, oversized chunks, and unrecognized
  section-header formats rather than silently dropping or corrupting
  content.

## Status

Core pipeline (extract -> chunk -> embed -> store -> retrieve -> generate)
is built and verified end-to-end against real Ollama models, with all 22
doctrine documents ingested and retrieval confirmed across the full set.
CLI and web GUI both working.

## Next steps

- Port to Raspberry Pi 5 (`poppler-utils` needed for `pdftotext`; Ollama
  models will need to fit Pi RAM/storage)
- `systemd` service for Pi deployment (auto-start on boot)
- Scenario-based training mode
- Read-only "document library" browsing view (separate from Q&A)
