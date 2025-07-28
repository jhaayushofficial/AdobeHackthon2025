# Use Python 3.10 on AMD64 platform
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and script into the container
COPY requirements.txt .
COPY process_pdfs.py .

# Install required packages
RUN pip install --no-cache-dir pymupdf

# Run the script on container start
CMD ["python", "process_pdfs.py"]
