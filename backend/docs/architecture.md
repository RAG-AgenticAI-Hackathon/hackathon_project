# Architecture Document
**Last Updated:** June 13, 2026

---
## Overview

This project allows users to ask questions about annual reports of Infosys, Amazon, and Alphabet.

The main goal is to avoid manually searching through hundreds of pages of reports. Instead, the system retrieves relevant sections and generates answers based only on the retrieved content.

For comparison-type questions, the system breaks the query into smaller parts and processes them separately before combining the results.

## Full Data Flow

```
User types a question
        │
        ▼
┌─────────────────┐
│   Router Agent  │  ← ROUTER_PROMPT_TEMPLATE
│  (SIMPLE or     │    Calls Claude to classify
│   COMPLEX?)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
SIMPLE     COMPLEX
    │         │
    │    ┌────▼──────────────────┐
    │    │  Sub-question Splitter │  ← SUB_QUESTION_SPLITTER_TEMPLATE
    │    │  Breaks into 2-3 Qs   │
    │    └────────────┬──────────┘
    │                 │ (one per company/year)
    │    ┌────────────▼──────────┐
    │    │  Run each sub-Q       │
    │    │  through retriever    │
    │    └────────────┬──────────┘
    │                 │
    ▼                 ▼
┌──────────────────────────────┐
│         retriever.py         │
│  1. Embed query (OpenAI)     │
│  2. Search ChromaDB (top-K)  │
│  3. Filter by threshold      │
│  4. Return chunks + scores   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       ChromaDB               │
│  Vector index of chunks      │
│  from all 3 annual reports   │
│  (created once by ingest.py) │
└──────────────┬───────────────┘
               │ (top-K chunks returned)
               ▼
┌──────────────────────────────┐
│          Claude LLM          │
│  RAG_PROMPT_TEMPLATE         │
│  + question + chunks         │
│  → generates answer          │
└──────────────┬───────────────┘
               │
               ▼ (for COMPLEX: combine sub-answers)
┌──────────────────────────────┐
│        api.py (FastAPI)      │
│  Returns JSON:               │
│  { answer, citations,        │
│    query_type, scores }      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       React Frontend         │
│  Displays answer + sources   │
└──────────────────────────────┘
```

---


## Key Design Decisions

### Choice of Vector Database

We selected ChromaDB because it is easy to set up and works locally without requiring any external service. Since this is a hackathon project, simplicity and fast development were more important than large-scale production features.

### Choice of text-embedding-3-small (not ada-002)?
It is Newer model (released 2024),Same quality, lower cost ($0.02 vs $0.10 per 1M tokens), Directly available via OpenAI Python SDK

### LLM Selection
Claude was chosen because it performs well on document-based question answering and follows instructions reliably when working with retrieved context.

### Chunking Strategy
We started with a chunk size of 500 tokens and an overlap of 50 tokens. These values provided a good balance between retrieval accuracy and context coverage during initial testing.

### Why an agentic router instead of just always searching all companies?
Since for simple questions, searching all 3 companies adds noise.The router makes the system faster and more precise.It demonstrates actual "agentic" behavior.

---