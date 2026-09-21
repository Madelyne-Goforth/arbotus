
import chromadb

class StoreDoctrine:
    def __init__(self, persist_dir, embed_fn):
        # store embed_fn; create chromadb.PersistentClient(path=str(persist_dir))
        # get_or_create_collection(name="army_doctrine")
        chromadb_client = chromadb.PersistentClient(path=str(persist_dir))
        collection = chromadb_client.get_or_create_collection(name="army_doctrine")
        self.chromadb_client = chromadb_client
        self.collection = collection
        self.embed_fn = embed_fn

    def add_chunks(self, chunks, batch_size=50):
        # Embed and upsert in small batches rather than one huge call --
        # sending hundreds of chunks to Ollama in a single request risks
        # timeouts/memory pressure on the embedding server (seen in practice
        # on larger doctrine docs). Batching also means a failure partway
        # through a doc does not lose the batches that already succeeded.
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]

            texts = [chunk.text for chunk in batch]
            embeddings = self.embed_fn(texts)
            ids = [chunk.chunk_id for chunk in batch]

            metadatas = [
                {
                    "doc_id": chunk.doc_id,
                    "doc_title": chunk.doc_title,
                    "section": chunk.section,
                    "source_url": chunk.source_url,
                    "pull_date": chunk.pull_date,
                    "chunk_index": chunk.chunk_index,
                    "access_tier": chunk.access_tier
                }
                for chunk in batch
            ]

            self.collection.upsert(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )

    def query(self, question, n_results=5):
        # embed the question with self.embed_fn
        # collection.query(...) with that embedding
        # return the results in a usable shape
        vector = self.embed_fn([question])[0]
        results = self.collection.query(
            query_embeddings=[vector],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        hits = []
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            hits.append({"text": doc, "metadata": meta, "distance": dist})
        return hits