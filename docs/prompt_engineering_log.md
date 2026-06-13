# Prompt Testing Notes

## RAG Prompt

Goal:
- Keep answers grounded in retrieved documents
- Avoid hallucinations
- Return a standard fallback response when information is unavailable

### Sample Tests

| Question | Result |
|-----------|---------|
| Infosys revenue FY2023 | Correct |
| Amazon business segments | Correct |
| Alphabet R&D spend 2022 | Correct |

## Router Prompt

Goal:
- Identify whether a query is simple or requires multi-company reasoning.

### Sample Tests

| Question | Classification |
|-----------|---------------|
| Infosys revenue? | SIMPLE |
| Compare Infosys and Amazon | COMPLEX |