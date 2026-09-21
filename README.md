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
docs_raw/*.txt --> chunker.py --> Chunk objects (schema.py)
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

python3 src/main.py ingest docs_raw/sample.txt \
  --doc-id AR670-1 \
  --title "Wear and Appearance of Army Uniforms and Insignia" \
  --url "https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN30964-AR_670-1-000-WEB-1.pdf"

python3 src/main.py ask "what's the fingernail standard for females"
```

## Adding doctrine

1. Pull a doctrine PDF from [armypubs.army.mil](https://armypubs.army.mil).
2. Extract its text to a `.txt` file under `docs_raw/` (manual copy-paste
   or `pdftotext` work for now -- section-structure-preserving PDF
   extraction is a later improvement, not yet built).
3. Ingest it with `main.py ingest` (see above), citing the real source
   URL and pull date.

The chunker splits on Army paragraph-header style (`3-4.`, `3-5.`, etc.)
via `SECTION_HEADER_RE` in `chunker.py` -- it'll need widening as
different doctrine documents break its current narrow assumption.

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

## Status

Core pipeline (chunk -> embed -> store -> retrieve -> generate) is built
and verified end-to-end against real Ollama models. CLI and web GUI both
working. Currently ingested: one short AR 670-1 excerpt (`docs_raw/sample.txt`)
-- broader doctrine coverage is next.

## Next steps

- Ingest a real, broader set of doctrine documents
- Section-aware PDF extraction (replace manual copy-paste)
- Widen `SECTION_HEADER_RE` as real docs break its current narrow assumption
- `systemd` service for Pi deployment (auto-start on boot)
- Scenario-based training mode
- Read-only "document library" browsing view (separate from Q&A)
