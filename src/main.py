"""
CLI entry point.

Usage:
    python3 main.py check
    python3 main.py ingest <path_to_txt> --doc-id AR670-1 --title "..." --url "..."
    python3 main.py ask "what's the fingernail standard for females"
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import ollama_client
from chunker import chunk_document
from vectorstore import StoreDoctrine
from mentor import ask, render_for_display

DATA_DIR = Path(__file__).parent.parent / "data" / "chroma"


def get_store() -> StoreDoctrine:
    # Builds a StoreDoctrine, wiring ollama_client.embed in as the embed_fn
    # StoreDoctrine's __init__ expects (dependency injection -- same pattern
    # discussed when vectorstore.py was written: StoreDoctrine doesn't know
    # or care that embeddings come from Ollama specifically, it just calls
    # whatever function it's handed).
    def embed_fn(texts: list[str]) -> list[list[float]]:
        return ollama_client.embed(texts)
    return StoreDoctrine(persist_dir=DATA_DIR, embed_fn=embed_fn)


def cmd_check(args):
    # Input: args -- argparse Namespace (unused here, check takes no flags)
    # Use case: `python3 main.py check`. Call ollama_client.check_connection(),
    #           print a clear reachable/not-reachable message. If not
    #           reachable, sys.exit(1) so scripts/CI can detect failure.
    if ollama_client.check_connection() == False:
        print("Not able to reach client.")
        sys.exit(1)
    else:
        print("Able to reach client.")


def cmd_ingest(args):
    # Input: args.file (str path), args.doc_id, args.title, args.url,
    #        args.pull_date (may be None -- default to today with
    #        date.today().isoformat() if so)
    # Use case: `python3 main.py ingest docs_raw/ar670-1.txt --doc-id ...`
    #           Read the file's text (Path.read_text()), pass it through
    #           chunk_document(...) to get a list of Chunk objects, then
    #           get_store().add_chunks(...) to embed + persist them.
    #           Print how many chunks were stored.

    # Find date or fix for none case
    if args.pull_date == None:
        date_pulled = date.today().isoformat()
    else:
        date_pulled = args.pull_date

    chunks = chunk_document(Path(args.file).read_text(), args.doc_id, args.title, args.url, date_pulled)

    get_store().add_chunks(chunks)
    print(f"{len(chunks)}")


def cmd_ask(args):
    # Input: args.question (str), args.model (str, has an argparse default)
    # Use case: `python3 main.py ask "..."`. get_store(), call ask(store,
    #           question, model=...), then print(render_for_display(result)).
    store = get_store()
    result = ask(store, args.question, model=args.model)
    print(render_for_display(result))


def main():
    parser = argparse.ArgumentParser(description="AR-BOTUS: offline doctrine RAG mentor")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="verify Ollama connectivity")
    p_check.set_defaults(func=cmd_check)

    p_ingest = sub.add_parser("ingest", help="chunk + embed + store a doctrine text file")
    p_ingest.add_argument("file", help="path to a .txt file of extracted doctrine text")
    p_ingest.add_argument("--doc-id", required=True, help='e.g. "AR670-1"')
    p_ingest.add_argument("--title", required=True, help="full document title")
    p_ingest.add_argument("--url", required=True, help="source URL on armypubs.army.mil")
    p_ingest.add_argument("--pull-date", default=None, help="ISO date, defaults to today")
    p_ingest.set_defaults(func=cmd_ingest)

    p_ask = sub.add_parser("ask", help="ask the mentor a question")
    p_ask.add_argument("question")
    p_ask.add_argument("--model", default="llama3.2:3b")
    p_ask.set_defaults(func=cmd_ask)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
