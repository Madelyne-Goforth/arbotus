# Inputs: text
# Outputs: Chunk instance (data + metadata)

# property chunk id:
    # combine doc_id, section, chunk_index into one raw string
    # hash that raw string (short, fixed length digest)
    # return f"{doc_id}_{section}_{digest}""


import hashlib

class Chunk:

    def __init__(self, text, doc_id, doc_title, section, source_url, pull_date, chunk_index = 0, access_tier = "public"):
        self.text = text
        self.doc_id = doc_id
        self.doc_title = doc_title
        self.section = section
        self.source_url = source_url
        self.pull_date = pull_date
        self.chunk_index = chunk_index
        self.access_tier = access_tier

    @property
    def chunk_id(self):
        # text, doc_id, doc_title, section, source_url, pull_date, chunk_index
        metadata = self.doc_id + self.section + str(self.chunk_index)
        hash_function = hashlib.sha1(metadata.encode()).hexdigest()[:8]
        return f"{self.doc_id}_{self.section}_{hash_function}"