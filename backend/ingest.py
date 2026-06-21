# ingest.py
# READ PDFs → CHUNK text → STORE in ChromaDB

import os
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer
import config

print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)

try:
    client.delete_collection(config.CHROMA_COLLECTION)
    print("Deleted old collection")
except:
    pass

collection = client.create_collection(
    config.CHROMA_COLLECTION,
    metadata={"hnsw:space": "cosine"},
)
print("Created fresh ChromaDB collection")

def chunk_text(text, chunk_size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

total_chunks = 0

company_folder = {
    "Infosys": "infosys",
    "Amazon": "amazon",
    "Alphabet": "alphabet",
}

for filename, metadata in config.DOC_METADATA.items():
    company = metadata["company"]
    folder = company_folder[company]
    pdf_path = os.path.join(config.PDF_DIR, folder, filename)

    if not os.path.exists(pdf_path):
        print(f"WARNING: {filename} not found at {pdf_path}, skipping...")
        continue

    print(f"\nProcessing {filename}...")

    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        print(f"  Extracted text from {len(pdf.pages)} pages")

    chunks = chunk_text(full_text)
    print(f"  Created {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk).tolist()
        collection.add(
            ids=[f"{metadata['company']}_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{
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