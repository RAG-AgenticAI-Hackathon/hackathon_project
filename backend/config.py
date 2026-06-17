"""
config.py
PURPOSE: Single source of truth for all tunable parameters.
"""
import os

# The three companies we support.
COMPANIES = ["infosys", "amazon", "alphabet"]

COMPANY_DISPLAY_NAMES = {
    "infosys": "Infosys",
    "amazon": "Amazon",
    "alphabet": "Alphabet (Google)",
}

# Maps filename -> company/year metadata (used by ingest.py)
DOC_METADATA = {
    "infosys_2023.pdf": {"company": "Infosys", "year": 2023},
}

# CHUNKING (used in ingest.py)
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# RETRIEVAL (used in retriever.py)
TOP_K = 5
SIMILARITY_THRESHOLD = 0.4

# MODELS
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # sentence-transformers, local, free
LLM_MODEL = "claude-sonnet-4-6"
LLM_MAX_TOKENS = 1024

# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE_DIR, "docs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
CHROMA_COLLECTION_NAME = "financial_reports"

# API KEY
from dotenv import load_dotenv
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

RAG_PROMPT_TEMPLATE = """You are a financial analyst assistant. Using ONLY the documents provided below, answer the question accurately and concisely.

Rules:
- Only use information present in the documents below. Do NOT use outside knowledge.
- If the documents do not contain enough information, say exactly: "I don't have enough information in the provided documents to answer this."
- Always mention which company the information came from.
- For numbers, be precise. Don't round unless the document rounds.

QUESTION: {question}

DOCUMENTS:
{context}

ANSWER:"""

ROUTER_PROMPT_TEMPLATE = """You are a query classifier for a financial document analysis system covering three companies: Infosys, Amazon, and Alphabet.

Classify the question as SIMPLE or COMPLEX.
SIMPLE = one company/metric. COMPLEX = comparison across companies or multiple lookups.

Respond ONLY in JSON like: {{"type": "SIMPLE", "companies": ["Infosys"]}}

Question: {question}"""

# API SETTINGS
API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["http://localhost:3000"]
