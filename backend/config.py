"""
config.py
PURPOSE: Single source of truth for all tunable parameters.
"""

# The three companies we support. 
COMPANIES = ["infosys", "amazon", "alphabet"]

# Maps company name → what to call it in answers

COMPANY_DISPLAY_NAMES = {
"infosys": "Infosys",
"amazon": "Amazon",
"alphabet": "Alphabet (Google)",
}

# CHUNKING (used in ingest.py)

CHUNK_SIZE = 500        # tokens per chunk
CHUNK_OVERLAP = 50   

# RETRIEVAL (used in retriever.py)

TOP_K = 5               
SIMILARITY_THRESHOLD = 0.6 

# MODELS

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "claude-3-5-sonnet-20241022"             
LLM_MAX_TOKENS = 1024  

# PATHS

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(BASE_DIR, "data", "pdfs")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
CHROMA_COLLECTION_NAME = "financial_reports" # The name of our collection inside ChromaDB


RAG_PROMPT_TEMPLATE = """You are a financial analyst assistant. Using ONLY the documents provided below, answer the question accurately and concisely.
Rules:
- Only use information present in the documents below. Do NOT use outside knowledge.
- If the documents do not contain enough information, say exactly: "I don't have enough information in the provided documents to answer this."
- Always mention which company the information came from.
- For numbers, be precise. Don't round unless the document rounds.
QUESTION: {question}
DOCUMENTS:
{retrieved_chunks}
ANSWER:"""
ROUTER_PROMPT_TEMPLATE = """You are a query classifier for a financial document analysis system covering three companies: Infosys, Amazon, and Alphabet.
Classify the user's question into ONE of these categories:
SIMPLE — The question asks about a single company, metric, or time period.
Examples:
  - "What was Infosys's revenue in FY2023?" → SIMPLE
  - "What are Amazon's business segments?" → SIMPLE
COMPLEX — The question requires comparing 2+ companies, multiple years, or calculations across documents.
Examples:
  - "Compare the net income of Infosys and Amazon." → COMPLEX
  - "Which company grew revenue fastest over 3 years?" → COMPLEX
Question: {question}
Reply with ONLY the word SIMPLE or COMPLEX. No explanation."""
SUB_QUESTION_SPLITTER_TEMPLATE = """You are a query decomposer for a financial document system.
The user asked a complex question requiring information from multiple sources.
Break it into 2-3 simple sub-questions that can each be answered independently.
Each sub-question must:
- Focus on ONE company or ONE year
- Be self-contained
- Use the exact company name: Infosys, Amazon, or Alphabet
Complex question: {question}
Reply ONLY with a numbered list of sub-questions. No explanation.
Example format:
1. What was Infosys's net income in FY2023?
2. What was Amazon's net income in FY2023?"""
# API SETTINGS
API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["http://localhost:3000"]   # React dev server
# Add live frontend URL before deployment
