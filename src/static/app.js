// AR-BOTUS frontend. Talks only to this same server's /ask endpoint --
// no external requests, fully offline. Deliberately dependency-free
// (no framework) since this is a single small page.

const form = document.getElementById("ask-form");
const input = document.getElementById("question-input");
const askButton = document.getElementById("ask-button");
const retrievedBody = document.getElementById("retrieved-body");
const mentorBody = document.getElementById("mentor-body");
const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

function setStatus(state, label) {
  statusDot.className = "status-dot " + state;
  statusText.textContent = label;
}

// Turns the retrieved_block string ("[doc_id §section] title (pulled ...\nexcerpt\n\n...")
// into lightly styled HTML: citation line highlighted, excerpt text plain.
// This is presentation-only -- it never changes what text is shown, only
// how it's wrapped in spans, so the retrieved/generated separation your
// backend guarantees is preserved all the way to the screen.
function renderRetrievedBlock(text) {
  if (!text || text.trim() === "No relevant doctrine found.") {
    return `<p class="placeholder">${text || "No relevant doctrine found."}</p>`;
  }
  const blocks = text.trim().split(/\n\n+/);
  return blocks
    .map((block) => {
      const lines = block.split("\n");
      const citationLine = lines[0];
      const excerpt = lines.slice(1).join("\n");
      return (
        `<span class="citation">${escapeHtml(citationLine)}</span>` +
        `<span class="excerpt-text">${escapeHtml(excerpt)}</span>`
      );
    })
    .join("\n");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function askQuestion(question) {
  setStatus("busy", "THINKING...");
  askButton.disabled = true;

  try {
    const resp = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!resp.ok) {
      throw new Error(`Server responded ${resp.status}`);
    }

    const result = await resp.json();

    retrievedBody.innerHTML = renderRetrievedBlock(result.retrieved_block);
    mentorBody.innerHTML = `<span class="mentor-text">${escapeHtml(result.generated || "")}</span>`;

    setStatus("ok", "READY");
  } catch (err) {
    mentorBody.innerHTML = `<p class="error-text">Request failed: ${escapeHtml(err.message)}. Is the Ollama server running?</p>`;
    setStatus("err", "ERROR");
  } finally {
    askButton.disabled = false;
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  askQuestion(question);
  input.value = "";
});

setStatus("ok", "READY");
