# chunks inputed text regs/doctrine into chunks (datatype w/metadata) for storage in vector db

import re
from schema import Chunk


def split_into_sections(raw_text):
    # Goal: Put into list of (section_number, section_text) pairs
    # Find all header matches with the regex
    # Text before the first match = section "0-0"
    # Each section runs from its header's start to the next header's start (or end of string, for the last one)

    pattern = r"^(\d+[-–—]\d+)[.,]\s+(?=[A-Za-z])"
    matches = list(re.finditer(pattern, raw_text, re.MULTILINE))

    pairVec = list()

    # front matter before the first header (if any) goes under "0-0"
    if matches and matches[0].start() > 0:
        pairVec.append(("0-0", raw_text[: matches[0].start()]))
    elif not matches:
        # no headers found at all -- whole doc is "0-0"
        pairVec.append(("0-0", raw_text))

    for idx, i in enumerate(matches):
        section_number = i.group(1)
        start = i.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw_text)
        section_text = raw_text[start:end]
        pairVec.append((section_number, section_text))

    return pairVec


# Safety cap: some documents have long table/appendix stretches with no
# recognizable "N-N." header at all, so a section can absorb way more text
# than intended -- sometimes tens of thousands of characters, which exceeds
# what the embedding model can handle in one call. Anything over this gets
# split into smaller pieces (still tagged with the same section number) so
# no single chunk sent to Ollama is ever too large.
MAX_CHUNK_CHARS = 6000


def _split_oversized(text, max_chars=MAX_CHUNK_CHARS):
    # Break long text into paragraph-bounded pieces, each under max_chars.
    paragraphs = text.split("\n\n")
    pieces = []
    current = ""
    for para in paragraphs:
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) > max_chars and current:
            pieces.append(current)
            current = para
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def chunk_document(raw_text, doc_id, doc_title, source_url, pull_date):
    # Goal: Turn into list[chunk]
    # Call split_into_sections
    # Build a Chunk instance for each (section_number, section_text) tuple,
    # splitting any oversized section into smaller pieces first
    # Skip anything basically empty (eg whitespace only)

    pairs = split_into_sections(raw_text)
    chunks = list()
    for section_number, section_text in pairs:

        if len(section_text.strip()) < 20:
            continue

        pieces = _split_oversized(section_text) if len(section_text) > MAX_CHUNK_CHARS else [section_text]

        for piece in pieces:
            chunks.append(
                Chunk(
                    text=piece,
                    doc_id=doc_id,
                    doc_title=doc_title,
                    section=section_number,
                    source_url=source_url,
                    pull_date=pull_date,
                    chunk_index=len(chunks),
                )
            )
    return chunks


if __name__ == "__main__":
    sample = (
        "AR 670-1\nWear and Appearance\n\n"
        "3-4. Hair standards\nHair will be neat.\n\n"
        "3-5. Fingernail standards\nKeep them trimmed.\n"
    )
    for section_number, section_text in split_into_sections(sample):
        print(f"--- {section_number} ---")
        print(section_text.strip())
        print()
