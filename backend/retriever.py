# retriever.py
# Given a question → search ChromaDB → return relevant chunks

import chromadb
from sentence_transformers import SentenceTransformer
import config

embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    config.CHROMA_COLLECTION,
    metadata={"hnsw:space": "cosine"},
)

def retrieve(question, companies=None):
    question_embedding = embedder.encode(question).tolist()

    where_filter = None
    if companies and len(companies) == 1:
        where_filter = {"company": companies[0]}

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=config.TOP_K,
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        similarity = 1 - dist
        if similarity >= config.SIMILARITY_THRESHOLD:
            chunks.append({
                "text": doc,
                "company": meta["company"],
                "year": meta["year"],
                "source": meta["source"],
                "similarity": round(similarity, 3)
            })

    return chunks


if __name__ == "__main__":
    question = "What is Infosys revenue in 2024?"
    print(f"Question: {question}\n")
    results = retrieve(question, companies=["Infosys"])
    if not results:
        print("No relevant chunks found!")
    else:
        print(f"Found {len(results)} relevant chunks:\n")
        for i, chunk in enumerate(results):
            print(f"--- Chunk {i+1} ---")
            print(f"Company: {chunk['company']} | Similarity: {chunk['similarity']}")
            print(f"Text preview: {chunk['text'][:200]}...")
            print()