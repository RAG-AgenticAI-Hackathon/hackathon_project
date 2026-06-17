# api.py
# This is the FastAPI backend — the "server" that listens for questions
# and returns AI-generated answers.
#
# Flow: User question → retriever.py finds chunks → Claude reads chunks → answer returned
#
# Person C's frontend will send a POST request to /ask and get back a JSON answer.

import json
import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import config
from retriever import retrieve

# --- Setup ---
app = FastAPI(title="Financial RAG API")
claude = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

# CORS allows Person C's frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production you'd restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request/Response shapes ---
class AskRequest(BaseModel):
    question: str  # what the user typed

class AskResponse(BaseModel):
    answer: str
    citations: list  # which chunks were used
    question_type: str  # SIMPLE or COMPLEX

# --- Router: decide if question is simple or complex ---
def classify_question(question: str) -> dict:
    """
    Ask Claude to classify the question.
    Returns: {"type": "SIMPLE", "companies": ["Infosys"]}
    """
    prompt = config.ROUTER_PROMPT_TEMPLATE.format(question=question)
    
    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.content[0].text.strip()
    
    try:
        return json.loads(raw)
    except:
        # fallback if Claude doesn't return clean JSON
        return {"type": "SIMPLE", "companies": ["Infosys"]}

# --- Main answer function ---
def get_answer(question: str, companies: list) -> tuple:
    """
    Retrieve relevant chunks and ask Claude to answer based on them.
    Returns (answer_text, citations_list)
    """
    # Get relevant chunks from ChromaDB
    chunks = retrieve(question, companies=companies)
    
    if not chunks:
        return "I don't have enough information to answer that question.", []
    
    # Build context string from chunks
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1} - {chunk['company']} {chunk['year']}]\n"
        context += chunk["text"] + "\n\n"
    
    # Ask Claude
    prompt = config.RAG_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )
    
    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.content[0].text.strip()
    
    # Build citations list for the frontend
    citations = [
        {
            "company": c["company"],
            "year": c["year"],
            "similarity": c["similarity"],
            "preview": c["text"][:150] + "..."
        }
        for c in chunks
    ]
    
    return answer, citations

# --- API Endpoints ---

@app.get("/")
def root():
    return {"status": "Financial RAG API is running!"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Step 1: classify the question
    classification = classify_question(question)
    question_type = classification.get("type", "SIMPLE")
    companies = classification.get("companies", ["Infosys"])
    
    # Step 2: for COMPLEX questions, get answers per company then combine
    if question_type == "COMPLEX":
        combined_answer = ""
        all_citations = []
        
        for company in companies:
            ans, cits = get_answer(question, companies=[company])
            combined_answer += f"**{company}:**\n{ans}\n\n"
            all_citations.extend(cits)
        
        return AskResponse(
            answer=combined_answer.strip(),
            citations=all_citations,
            question_type="COMPLEX"
        )
    
    # Step 3: SIMPLE — just answer directly
    answer, citations = get_answer(question, companies=companies)
    
    return AskResponse(
        answer=answer,
        citations=citations,
        question_type="SIMPLE"
    )