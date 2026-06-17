# Judge Q&A Preparation

Likely questions and short, confident answers. Memorize these — don't read them.

---

## Q1: "Why not just use ChatGPT with document upload?"
**Answer:**
> "ChatGPT's document upload has a context window limit — it can't hold three full annual reports at once. Our system chunks, embeds, and retrieves only the relevant passages at query time, so it scales to much larger document sets. Also, our citations are traceable — you can read the exact source passage. ChatGPT doesn't show you that."

---

## Q2: "How does it handle follow-up questions?"
**Answer:**
> "Right now it doesn't maintain conversation history — each question is independent. That's a known limitation we'd add in the next sprint: pass the last 2-3 message turns as context. We prioritized RAG accuracy and citation quality over conversation memory for this hackathon."

---

## Q3: "How would this scale to more companies or longer documents?"
**Answer:**
> "ChromaDB is just a local vector store here. Swapping it for Pinecone or Weaviate takes a config change — the retrieval logic is identical. For more documents, we'd just run ingest.py again. The bottleneck is embedding time, which is one-off per document. Query time stays fast regardless of document count."

---

## Q4: "How accurate is it? Did you test for hallucinations?"
**Answer:**
> "We ran five stress tests — simple Q&A, multi-company comparison, ambiguous questions, calculations, and out-of-scope questions. Four of five passed. The system is grounded because the LLM prompt explicitly says 'only use the documents below' and returns a standard failure phrase when it can't answer — which triggers the styled error card you saw. We don't claim 100% accuracy, but every answer is traceable to a source."

---

## Q5: "Why Anthropic Claude instead of OpenAI?"
**Answer:**
> "Claude follows document-grounded instructions more reliably in our testing — it's less likely to add outside knowledge when told to use only the provided context. It also has a longer context window for handling large retrieved passages. And the Anthropic API pricing for our use case was comparable."

---

## Q6: "What's the business case? Who pays for this?"
**Answer:**
> "Equity research analysts spend 40-60% of their time on document search. This compresses that to seconds. Potential customers: hedge funds, investment banks, IRR teams, compliance departments. Subscription SaaS model — per-user or per-company-portfolio pricing. The financial data intelligence market is $9B+ globally."

---

## Q7: "Why three companies? Why not more?"
**Answer:**
> "Three is a deliberate scope choice for the hackathon to show the system works cleanly. The architecture supports any number — adding a new company is: download PDF, add one line to DOC_METADATA in config.py, re-run ingest.py. Five minutes per company."

---

## If you don't know the answer:
> "That's a great question — [Person B / Person A] can speak to that more precisely. What I can tell you from the UI side is..."
→ Always redirect to a teammate rather than guessing.
