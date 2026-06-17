# api.py
# FastAPI backend using Groq (free, fast LLM API)
# Flow: question → router → retriever → Groq LLM → answer

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# --- Helper: call Groq LLM ---
def call_llm(prompt: str, max_tokens: int = 1024) -> str:
    response = groq_client.chat.completions.create(
       model="llama-3.3-70b-versatile",  # free, fast, good quality
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.1,          # low = more factual, less creative
    )
    return response.choices[0].message.content.strip()

# --- Router: classify question as SIMPLE or COMPLEX ---
def classify_question(question: str) -> dict:
    prompt = config.ROUTER_PROMPT_TEMPLATE.format(question=question)
    raw = call_llm(prompt, max_tokens=100)
    
    # clean markdown if model wraps in ```json
    raw = raw.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(raw)
    except:
        return {"type": "SIMPLE", "companies": ["Infosys"]}

# --- Main answer function ---
def get_answer(question: str, companies: list) -> tuple:
    chunks = retrieve(question, companies=companies)
    
    if not chunks:
        return "I don't have enough information in the provided documents to answer this.", []
    
    # Build context from retrieved chunks
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1} - {chunk['company']} {chunk['year']}]\n"
        context += chunk["text"] + "\n\n"
    
    prompt = config.RAG_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )
    
    answer = call_llm(prompt)
    
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