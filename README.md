# RAG_AgenticAI_Hackathon
# Financial RAG Chatbot

> An agentic Retrieval-Augmented Generation system for financial document analysis across Infosys, Amazon, and Alphabet annual reports.

---

## 1. Problem Statement

Annual reports contain a large amount of financial information, finding a specific detail in it is very difficult.

This project allows users to ask questions about the annual reports of Infosys, Amazon, and Alphabet. The system retrieves relevant sections from the reports and generates answers based only on the retrieved information.

For comparison-based questions, the system can break the query into smaller tasks and combine the results into a single response.
---

## 2. Architecture


**Data Flow:**
```
User Question
     ↓
Router Agent (SIMPLE or COMPLEX?)
     ↓                    ↓
Single Company         Multi-Company
Retriever              Sub-question Split
     ↓                    ↓
ChromaDB Search    ChromaDB Search × N
     ↓                    ↓
Top-K Chunks       Merge Chunks
     ↓                    ↓
         LLM (Claude)
              ↓
     Answer + Citations
```

---

## 3. Tech Stack

## Technologies Used

| Technology | Purpose |
|------------|----------|
| pdfplumber | Extracting text from annual reports |
| OpenAI Embeddings | Converting document chunks into vector embeddings |
| ChromaDB | Storing and searching embeddings |
| Claude | Generating answers from retrieved content |
| FastAPI | Backend API development |
| React | Building the user interface |
| Render | Backend deployment |
| Vercel | Frontend deployment |

---

## 4. How to Run

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API key (for embeddings)
- Anthropic API key (for LLM)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys in .env
python ingest.py        # Step 1: Ingest PDFs into ChromaDB
python api.py           # Step 2: Start FastAPI server
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 5. Example Questions

## Sample Questions

- What was Infosys's revenue in FY2023?
- What are Amazon's major business segments?
- How much did Alphabet spend on research and development?
- Compare the latest net income of Infosys and Amazon.
- Which company showed the highest revenue growth?


## 7. Deployment

- **Backend live URL:** 
- **Frontend live URL:** 

---

## Team

- Architecture and RAG Design
- Backend Development
- Frontend Development and Presentation
