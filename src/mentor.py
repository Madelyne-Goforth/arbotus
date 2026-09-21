from ollama_client import chat
from vectorstore import StoreDoctrine


def format_retrieved_block(hits: list[dict]) -> str:
    # Input: hits = the list of hit-dicts returned by StoreDoctrine.query()
    #        (each dict has "text", "metadata", "distance")
    # Output: a single string containing all retrieved excerpts, citation-tagged
    #         (doc_id, section, doc_title, pull_date, source_url pulled from metadata)
    # Use case: called first inside ask(), BEFORE the LLM ever runs -- this is what
    #           guarantees "retrieved doctrine" is rendered by deterministic code,
    #           never by the model itself. Handle the empty-hits case too.
    string = str("") 
    for hit in hits:
        # make a string
        local_string = (
            f"[{hit['metadata']['doc_id']} §{hit['metadata']['section']}] "
            f"{hit['metadata']['doc_title']} "
            f"(pulled {hit['metadata']['pull_date']}, source: {hit['metadata']['source_url']})\n"
            f"{hit['text']}"
        )
        local_string += "\n\n"
        # append it
        string += local_string
    if string == "":
        return str("No relevant doctrine found.")
    else:
        return string


# Not a function -- a module-level string constant.
# Use case: passed as the "content" of the {"role": "system", ...} message every
#           time ask() calls chat() => establishes the PSG-mentor persona and
#           behavioral rules (Socratic by default, never contradicts retrieved
#           doctrine, admits when retrieved material doesn't fully answer,
#           never invents a citation) for every response.
MENTOR_SYSTEM_PROMPT = """\
You are a senior NCO (Platoon Sergeant) mentoring a new Lieutenant who just \
took over as Platoon Leader. Your job is not to hand over answers -- it's to \
develop their judgment, the way a good PSG breaks in a new LT.

How you'll receive information:
Before the LT's question, you will be given a block of retrieved doctrine \
excerpts, each formatted as "[doc_id \u00a7section] doc_title (pulled date, \
source: url)" followed by the excerpt text. Treat ONLY this retrieved block \
as ground truth. If it instead reads "No relevant doctrine found.", nothing \
matched the question -- say so plainly, do not guess or fall back on your \
own general knowledge of Army policy.

Behavioral rules:
1) Never contradict the retrieved doctrine.
2) If the retrieved excerpts don't fully answer the question, say so plainly
   instead of filling the gap with a guess -- including when nothing was
   retrieved at all.
3) Never invent a citation or section number. Only reference sections that
   appear in the retrieved excerpts you were given.
4) Default to Socratic: ask a clarifying or probing question back before
   just handing over the answer -- UNLESS the question is time-sensitive or
   a direct factual lookup (e.g. "what's the exact standard for X"), in
   which case give the straight answer first, then the deeper "why it
   matters" point.
5) Speak like an experienced, no-nonsense but genuinely invested mentor.
   Direct, a little dry, zero condescension. You want this LT to succeed.
"""


def ask(store: StoreDoctrine, question: str, model: str = "llama3.2:3b") -> dict:
    # Input: store = a StoreDoctrine instance, already populated with ingested doctrine
    #        question = the user's question, as a string
    #        model = optional override, defaults to "llama3.2:3b"
    # Output: a dict, at minimum {"question": ..., "retrieved_block": ..., "generated": ...}
    # Use case: the orchestrator => retrieval -> block-formatting -> prompt assembly ->
    #           generation, in one call. main.py's `ask` subcommand calls this directly.
    to_return = {}

    # Store retrieved block
    retrieved_block = store.query(question, n_results = 5)
    formatted_retrieved_block = format_retrieved_block(retrieved_block)

    # Build messages
    messages = []
    messages = [
        {"role": "system", "content": MENTOR_SYSTEM_PROMPT},
        {"role": "user", "content": f"{formatted_retrieved_block}\n\nLT's question: {question}"}
    ]

    generated = chat(messages, model=model)
    
    to_return = {
        "question": question,
        "retrieved_block": formatted_retrieved_block,
        "generated": generated
    }
    
    return to_return


def render_for_display(result: dict) -> str:
    # Input: result = the dict ask() returns
    # Output: a single human-readable string, formatted for terminal printing, with
    #         a visible divider between retrieved doctrine and generated commentary
    # Use case: called right after ask() in main.py, purely for presentation -- keeps
    #           display formatting separate from retrieval/generation logic, so ask()
    #           stays reusable for a different output format later (e.g. a web UI)
    divider = "=" * 60
    return (
        f"{divider}\n"
        f"{result['retrieved_block']}\n"
        f"{divider}\n"
        f"MENTOR (AI-generated, grounded in the above):\n\n"
        f"{result['generated']}\n"
    )
