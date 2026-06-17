# ingest.py
# This file does 3 things:
# 1. READ — extract raw text from PDFs using pdfplumber
# 2. CHUNK — split text into small overlapping pieces
# 3. STORE — convert chunks to embeddings and save in ChromaDB

import os
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer
import config

# --- Step 1: Load the embedding model ---
# This model converts text → list of numbers (called a vector/embedding)
# Similar text will produce similar numbers — that's how semantic search works
print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, good quality

# --- Step 2: Connect to ChromaDB ---
client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)

# Delete old collection if it exists (so we start fresh each run)
try:
    client.delete_collection(config.CHROMA_COLLECTION)
    print("Deleted old collection")
except:
    pass

collection = client.create_collection(config.CHROMA_COLLECTION)
print("Created fresh ChromaDB collection")

# --- Step 3: Define chunking function ---
def chunk_text(text, chunk_size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP):
    """
    Splits a long string into overlapping chunks.
    
    Example with chunk_size=10, overlap=3:
    "Hello World Foo Bar" → ["Hello Worl", "orld Foo B", "o Bar"]
    
    Overlap ensures a sentence cut at a boundary isn't lost.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # move forward but overlap a bit
    return chunks

# --- Step 4: Process each PDF ---

docs_path = os.path.join(config.BASE_DIR, "data", "pdfs")
total_chunks = 0

for filename, metadata in config.DOC_METADATA.items():
    pdf_path = os.path.join(docs_path, filename)
    
    if not os.path.exists(pdf_path):
        print(f"WARNING: {filename} not found, skipping...")
        continue
    
    print(f"\nProcessing {filename}...")
    
    # Extract text from every page
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        print(f"  Extracted text from {len(pdf.pages)} pages")
    
    # Chunk the text
    chunks = chunk_text(full_text)
    print(f"  Created {len(chunks)} chunks")
    
    # Embed and store each chunk in ChromaDB
    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk).tolist()  # convert numpy array to list
        
        collection.add(
            ids=[f"{metadata['company']}_{i}"],           # unique ID for each chunk
            embeddings=[embedding],                         # the vector
            documents=[chunk],                              # original text
            metadatas=[{                                    # extra info we can filter by
                "company": metadata["company"],
                "year": metadata["year"],
                "chunk_index": i,
                "source": filename
            }]
        )
    
    total_chunks += len(chunks)
    print(f"  Stored {len(chunks)} chunks for {metadata['company']}")

print(f"\nDone! Total chunks stored: {total_chunks}")
print("ChromaDB is ready at:", config.CHROMA_DB_PATH)