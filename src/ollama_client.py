
import requests

OLLAMA_HOST = "http://localhost:11434"

# Turns doctrine (chunked text)and user messages into (embeded) vectors 
def embed(texts: list[str], model: str = "nomic-embed-text") -> list[list[float]]:
    # Input: texts: list of strings (the chunk texts, or a single question wrapped in a one-item list)
    # model (string), defaults to "nomic-embed-text"
    # Outputs: a list of vectors (eg list[list[float]]), one vector per input text, same ordering essentially

    # Embed each text in the list using Ollama's embedding model
    response = requests.post(f"{OLLAMA_HOST}/api/embed", json={"model": model, "input": texts})
    if not response.ok:
        # raise_for_status() alone hides Ollama's actual error message --
        # surface it so a bad request is debuggable instead of a bare 400.
        raise requests.exceptions.HTTPError(
            f"{response.status_code} error from Ollama /api/embed: {response.text[:500]}"
        )
    return response.json()["embeddings"]  # Return the list of embeddings from the response

# produces the mentor's response text to a user question
def chat(messages: list[dict], model: str = "llama3.2:3b") -> str:
    # Input: messages: list of dicts, each shaped {"role": "system"|"user"|"assistant", "content": "..."}
    # model (string), defaults to "llama3.2:3b"
    # Output: a single string -- just the assistant's reply content, not the whole response envelope
    response = requests.post(f"{OLLAMA_HOST}/api/chat", json={"model": model, "messages": messages, "stream": False})
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()["message"]["content"]  # Return the assistant's reply content

# Checks if Ollama is running and responding
def check_connection() -> bool:
    # Input: none
    # Output: a single bool -- True if Ollama responded, False if the request failed for any reason
    #         (server not running, timeout, etc.) -- wrap the request in try/except
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
        return r.ok
    except requests.RequestException:
        return False
