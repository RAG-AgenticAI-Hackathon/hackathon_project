"""
config.py
PURPOSE: Single source of truth for all tunable parameters.
"""
import os
from dotenv import load_dotenv
load_dotenv()

#Companies 

COMPANIES = ["infosys", "amazon", "alphabet"]

COMPANY_DISPLAY_NAMES = {
    "infosys": "Infosys",
    "amazon": "Amazon",
    "alphabet": "Alphabet (Google)",
}

#PDF Metadata 

DOC_METADATA = {
    "infosys_2024.pdf":  {"company": "Infosys",  "year": 2024},
    "amazon_2023.pdf":   {"company": "Amazon",   "year": 2023},
    "alphabet_2023.pdf": {"company": "Alphabet", "year": 2023},
}

#Chunking (used in ingest.py) 

CHUNK_SIZE = 400        # characters per chunk
CHUNK_OVERLAP = 50    # overlap between chunks

#Retrieval (used in retriever.py)

TOP_K = 5
SIMILARITY_THRESHOLD = 0.1

#Models 

EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # runs locally, no API key needed
LLM_MODEL = "claude-sonnet-4-6"
LLM_MAX_TOKENS = 1024

#Paths ─

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR  = os.path.join(BASE_DIR, "data", "pdfs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
CHROMA_COLLECTION_NAME = "financial_reports"

# Aliases used by ingest.py and retriever.py
CHROMA_DB_PATH   = CHROMA_DIR
CHROMA_COLLECTION = CHROMA_COLLECTION_NAME

#API Keys

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

#Prompts 

RAG_PROMPT_TEMPLATE = """You are a financial analyst assistant. Using ONLY the documents provided below, answer the question accurately and concisely.

Rules:
- Only use information present in the documents below. Do NOT use outside knowledge.
- If the documents do not contain enough information, say exactly: "I don't have enough information in the provided documents to answer this."
- Always mention which company the information came from.
- For numbers, be precise. Don't round unless the document rounds.
- If the question is not about Infosys, Amazon, or Alphabet financials, say: "This question is outside the scope of the provided documents."
- If asked to compare, extract the specific metric for the company mentioned in the source documents and state it clearly with the company name.
QUESTION: {question}

DOCUMENTS:
{context}

ANSWER:"""

ROUTER_PROMPT_TEMPLATE = """You are a query classifier for a financial document analysis system covering three companies: Infosys, Amazon, and Alphabet.

Classify the question as SIMPLE or COMPLEX.

SIMPLE = question about one company only.
COMPLEX = comparison across 2 or more companies.

For COMPLEX questions, always include ALL relevant companies.

Examples:
- "What was Infosys revenue?" → {{"type": "SIMPLE", "companies": ["Infosys"]}}
- "What are Amazon segments?" → {{"type": "SIMPLE", "companies": ["Amazon"]}}
- "Compare Infosys and Amazon net income" → {{"type": "COMPLEX", "companies": ["Infosys", "Amazon"]}}
- "Which company had highest growth?" → {{"type": "COMPLEX", "companies": ["Infosys", "Amazon", "Alphabet"]}}

Question: {question}

Respond ONLY in JSON. No explanation."""


SUB_QUESTION_SPLITTER_TEMPLATE = """You are a query decomposer for a financial document system.

Break the complex question into 2-3 simple sub-questions that can each be answered independently.

Each sub-question must:
- Focus on ONE company or ONE year
- Be self-contained
- Use the exact company name: Infosys, Amazon, or Alphabet
- Be answerable WITHOUT knowing the other sub-questions

Complex question: {question}

Reply ONLY with a numbered list. No explanation.
Example:
1. What was Infosys's net income in FY2024?
2. What was Amazon's net income in FY2023?"""


#API Settings 

API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["http://localhost:3000"]
GROQ_API_KEY = os.getenv("GROQ_API_KEY")