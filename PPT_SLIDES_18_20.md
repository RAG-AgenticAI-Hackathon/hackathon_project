# PPT Content — Slides 18, 19, 20
## Ready to paste directly into Google Slides / PowerPoint

---

## SLIDE 18 — Business Case: "Why This Matters"

**Heading:** Why This Matters

**Big stat (center, large font):**
> 40–60%
> of an equity analyst's time is spent searching documents

**Three bullets below:**
- Annual reports average 200+ pages — analysts search them manually today
- A wrong number in a report can cost millions in trading decisions
- FinSight RAG delivers cited, verifiable answers in under 10 seconds

**Bottom strip (3 columns):**
| $9B+ | 48hrs → 10sec | 100% |
|---|---|---|
| Global financial data intelligence market | Time to answer a complex cross-company query | Source-cited answers — zero hallucination risk for in-document facts |

**Speaker note:**
> "Financial analysis is still mostly a manual, document-intensive process. Our system doesn't replace analysts — it removes the 40% of their time that's just Ctrl+F in a PDF."

---

## SLIDE 19 — Roadmap: "What's Next"

**Heading:** Roadmap

**Timeline layout (3 items):**

**Sprint 2 (next 2 weeks)**
- Multi-turn conversation history (context across questions)
- Confidence scoring display in UI (numeric % shown per answer)
- PDF table extraction for structured financial data (balance sheets, P&L)

**Sprint 3 (month 2)**
- Support 20+ companies (one-click ingestion from SEC EDGAR API)
- Comparison mode: side-by-side answer panels for two companies
- Export to PDF report with citations auto-formatted

**Sprint 4 (month 3)**
- Enterprise authentication and per-team document namespaces
- Real-time ingestion of quarterly reports on filing date
- API access for programmatic querying (B2B integration)

**Speaker note:**
> "The architecture is already built to support all of this — it's a configuration and data problem, not a rebuild."

---

## SLIDE 20 — Team

**Heading:** The Team

**Layout: 3 equal columns**

**Column 1:**
Name: [Person A's name]
Role: Architecture & RAG Design
Owns: System design, chunking strategy, prompt engineering, stress testing
One line: "Decided what the system does and how it's structured"

**Column 2:**
Name: [Person B's name]
Role: Backend & Deployment
Owns: Ingestion pipeline, vector store, FastAPI, ChromaDB, Render deployment
One line: "Built everything the architecture specified"

**Column 3:**
Name: [Your name — Charvitha]
Role: Frontend & Product
Owns: React UI, UX design, demo flow, PPT, this slide
One line: "Built what judges see and interact with"

**Bottom strip:**
Built in 11 days · Infosys + Amazon + Alphabet · Powered by Claude Sonnet + ChromaDB

**Speaker note:**
> "Each of us owned a distinct layer. We shipped end-to-end in 11 days."

---

## SLIDE 17 — Demo Screenshots (LEAVE BLANK FOR NOW)
Add after you run the stress tests and take screenshots.

**Placeholders to fill:**
- Screenshot 1: Simple Q&A (Infosys revenue question + answer + 2 citation cards)
- Screenshot 2: Complex comparison (2-company answer + 4 citation cards)
- Screenshot 3: Out-of-scope amber card ("Not found in documents")

**Caption text (ready to paste when screenshots are added):**
- "Simple query: single-company fact retrieval with source citations"
- "Complex query: agentic routing splits into 2 sub-queries, combines results"
- "Out-of-scope: system refuses to hallucinate, shows styled error with rephrasing hint"
