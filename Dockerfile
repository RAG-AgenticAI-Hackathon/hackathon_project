FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r backend/requirements.txt

RUN cd backend && python ingest.py

CMD cd backend && uvicorn api:app --host 0.0.0.0 --port $PORT
