"""
Local web GUI for AR-BOTUS. A Flask server running on localhost, calling
the exact same mentor.ask() the CLI uses => this is a thin presentation
layer, not a second copy of the RAG logic. Fully offline: Flask serves
the page to your own browser over localhost, no external requests.

Run with: python3 src/app.py
Then open http://localhost:5000 in a browser.
"""

from flask import Flask, render_template, request, jsonify

import ollama_client
from vectorstore import StoreDoctrine
from mentor import ask
from main import DATA_DIR  # reuse the same persist path the CLI uses

app = Flask(__name__)

# Build ONE StoreDoctrine when the server starts, not one per request --
# same embed_fn dependency-injection pattern as main.py's get_store().
# Use case: every route below reuses this single `store` instead of
#           reconnecting to Chroma on every request.
def embed_fn(texts: list[str]) -> list[list[float]]:
    return ollama_client.embed(texts)

store = StoreDoctrine(persist_dir=DATA_DIR, embed_fn=embed_fn)


@app.route("/")
def index():
    # Use case: serves the chat page itself (templates/index.html).
    # Nothing to fill in here -- render_template() is one line, already
    # written below. The page's JS will call /ask via fetch().
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask_route():
    # Input: JSON POST body -- {"question": "..."}. Read it with
    #        request.get_json() (returns a dict, use ["question"] or
    #        .get("question") on it).
    # Output: JSON response the frontend JS can render into two panes.
    #         Reuse ask()'s own return shape directly -- it already has
    #         "question", "retrieved_block", "generated" as separate
    #         keys, which is exactly what a split retrieved/generated
    #         UI needs. Don't run it through render_for_display() here --
    #         that function mixes the two into one terminal string, which
    #         is the opposite of what a two-pane GUI wants.
    # Use case: call ask(store, question), then return jsonify(result).
    #           Optional but worth it: wrap in try/except so a model or
    #           connection error becomes a clean JSON error response
    #           instead of a raw Flask 500 page.
    requested = request.get_json()["question"]
    requested_result = ask(store, requested)
    return jsonify(requested_result)


if __name__ == "__main__":
    import os
    import webbrowser

    # In Flask's debug mode, the reloader restarts this process in a child
    # process -- WERKZEUG_RUN_MAIN is only set in that real, final process,
    # not in the initial one that just launches the reloader. Checking it
    # keeps the browser from popping open twice on every code change.
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        webbrowser.open("http://localhost:5000")

    app.run(debug=True, port=5000)
