# retriever.py
# This file answers the question: "Given a user's question, which chunks are most relevant?"
# It does NOT call Claude yet — it just finds the right pieces of text from ChromaDB.

import chromadb
from sentence_transformers import SentenceTransformer
import config

# Load the same embedding model we used in ingest.py
# IMPORTANT: must be the same model, otherwise the numbers won't match
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to the existing ChromaDB (already filled by ingest.py)
client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
collection = client.get_collection(config.CHROMA_COLLECTION)

def retrieve(question, companies=None):
    """
    Given a question, find the most relevant chunks from ChromaDB.
    
    How it works:
    1. Convert the question into an embedding (vector of numbers)
    2. ChromaDB finds stored chunks whose embeddings are closest to the question's embedding
    3. Return those chunks with their scores and metadata
    
    'companies' is an optional filter — e.g. ["Infosys"] to only search Infosys docs
    """
    
    # Step 1: embed the question
    question_embedding = embedder.encode(question).tolist()
    
    # Step 2: build optional company filter
    where_filter = None
    if companies and len(companies) == 1:
        where_filter = {"company": companies[0]}
    
    # Step 3: search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=config.TOP_K,
        where=where_filter,  # None means search all companies
        include=["documents", "metadatas", "distances"]
    )
    
    # Step 4: filter out chunks that are too dissimilar
    # ChromaDB returns "distances" — lower = more similar
    # We convert distance to similarity: similarity = 1 - distance
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


# --- Quick test (only runs when you execute this file directly) ---
if __name__ == "__main__":
    question = "What is Infosys revenue in 2023?"
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