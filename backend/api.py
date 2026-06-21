# api.py
# This is the FastAPI backend — the "server" that listens for questions
# and returns AI-generated answers.
#
# Flow: User question → retriever.py finds chunks → LLM reads chunks → answer returned
#
# Person C's frontend will send a POST request to /ask and get back a JSON answer.

import json
from groq import Groq
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import config
from retriever import retrieve

# --- Setup ---
app = FastAPI(title="Financial RAG API")
groq_client = Groq(api_key=config.GROQ_API_KEY)
LLM_MODEL = config.LLM_MODEL

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request/Response shapes ---
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    citations: list
    question_type: str

# --- Router: decide if question is simple or complex ---
def classify_question(question: str) -> dict:
    """
    Ask the LLM to classify the question.
    Returns: {"type": "SIMPLE", "companies": ["Infosys"]}
    """
    prompt = config.ROUTER_PROMPT_TEMPLATE.format(question=question)

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        max_tokens=200,
        temperature=0.1,   # low = more factual, less creative
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except:
        # fallback if the model doesn't return clean JSON
        return {"type": "SIMPLE", "companies": ["Infosys"]}

# --- Main answer function ---
def get_answer(question: str, companies: list) -> tuple:
    """
    Retrieve relevant chunks and ask the LLM to answer based on them.
    Returns (answer_text, citations_list)
    """
    # Get relevant chunks from ChromaDB
    chunks = retrieve(question, companies=companies)
    
    if not chunks:
        return "I don't have enough information in the provided documents to answer this.", []
    
    # Build context from retrieved chunks
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1} - {chunk['company']} {chunk['year']}]\n"
        context += chunk["text"] + "\n\n"
    
    # Ask the LLM
    prompt = config.RAG_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        max_tokens=1000,
        temperature=0.1,   # low = more factual, less creative
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content.strip()

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
    
    # Step 1: classify
    classification = classify_question(question)
    question_type = classification.get("type", "SIMPLE")
    companies = classification.get("companies", ["Infosys"])
    
    # Step 2: COMPLEX — answer per company and combine
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
    
    # Step 3: SIMPLE — answer directly
    answer, citations = get_answer(question, companies=companies)
    
    return AskResponse(
        answer=answer,
        citations=citations,
        question_type="SIMPLE"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)