FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu \
    sentence-transformers \
    chromadb \
    fastapi \
    uvicorn \
    pdfplumber \
    groq \
    python-dotenv \
    pydantic

RUN cd backend && python ingest.py

CMD ["sh", "-c", "cd backend && uvicorn api:app --host 0.0.0.0 --port $PORT"]