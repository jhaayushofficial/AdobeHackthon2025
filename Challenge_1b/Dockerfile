FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY process_documents.py .

RUN pip install --no-cache-dir pymupdf

CMD ["python", "process_documents.py", "/app/input"]
