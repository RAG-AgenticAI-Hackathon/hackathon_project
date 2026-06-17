# Demo Script — Person C (5 minutes)

## Setup (before judges walk in)
- Clear browser history / open fresh tab
- Open: http://localhost:5173 (or live Vercel URL)
- Have this script open on your phone (not on the demo screen)
- Test one question 10 minutes before to warm up the API

---

## Your Opening Line (say this while pointing at the screen)
> "I built the user interface. Let me show you how a judge or analyst would actually use this — and what makes it different from just asking ChatGPT."

---

## Question 1 — SIMPLE (30 seconds)

**Type:** `What was Infosys revenue in FY2024?`

**While it loads, say:**
> "Notice the three bouncing dots — the system is retrieving chunks from the actual Infosys annual report. Not the internet. Not hallucinated data."

**When answer appears, point out:**
- The answer text reveals word by word (streaming feel)
- The gray citation cards below — "these are the exact passages retrieved"
- Click one card to expand it — "you can verify every sentence against the source document"

---

## Question 2 — COMPLEX (90 seconds — the main demo moment)

**Type:** `Compare operating margins of Infosys and Amazon`

**While it loads (takes ~8-10 seconds), say:**
> "This is where the agentic routing kicks in. The system classified this as a COMPLEX question — it needs to search two separate companies' documents and combine the results. Watch what happens."

**When answer appears:**
- Show the two-part answer (Infosys section + Amazon section)
- Point to the 4 citation cards — "two from Infosys, two from Amazon — each one retrievable and verifiable"
- Say: *"A regular ChatGPT wouldn't ground this in documents. We do."*

---

## Question 3 — OUT OF SCOPE (45 seconds — shows robustness)

**Type:** `Who is the best tech company to invest in?`

**When the amber card appears, say:**
> "This question isn't answerable from the documents — and the system knows that. It doesn't hallucinate an answer. It tells you exactly why it can't help and suggests how to rephrase. That's contextual fidelity — one of the core evaluation criteria for this hackathon."

---

## Closing Line (15 seconds)
> "The UI is designed so judges can verify every answer — citations are expandable, confidence is visible, and failure states are explicit. No black box."

---

## If the demo crashes / API is slow:
> "Let me show you what this looks like from a screenshot while it loads..."
> → Open `stress_test_screenshots/` folder and show the PNG files

---

## Timing Check
| Section | Time |
|---|---|
| Opening line | 15s |
| Q1 simple | 60s |
| Q2 complex | 90s |
| Q3 out of scope | 45s |
| Closing | 15s |
| **Total** | **~3m 45s** |
Leaves ~75 seconds buffer for questions or slowness.
