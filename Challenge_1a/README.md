**[TEAM PHOENIX]**
Team Leader: Arsh Chaudhary
Team Member-1: Anushka Mittal
Team Member-2: Mishthi Goel 


# Adobe Hackathon 2025 – Challenge 1A  
## Structured PDF Outline Extraction Engine

This project is a fully containerized PDF processing pipeline built for Challenge 1A of the Adobe India Hackathon 2025. It extracts a structured outline — including the document title and hierarchical headings (H1, H2, H3) — from each input PDF and outputs it in a compliant JSON format.

---

## 🔍 Problem Overview

The goal was to design a robust system that takes unstructured PDF files and outputs structured outlines representing the semantic hierarchy of the content. The system must:
- Automatically process all PDFs from a specified input folder
- Identify the title, H1, H2, H3 headers
- Output valid .json files conforming to a given schema
- Operate fully offline in a restricted CPU-only environment
- Complete execution in under 10 seconds for a 50-page document

---

## 🧠 Key Features

- Custom PDF Outline Analyzer: Processes visual structure and content patterns to derive heading hierarchies
- Smart Heuristics Engine: Detects section headers and distinguishes text levels by analyzing styles, size, and placement
- JSON Generator: Converts the extracted outline into schema-compliant output
- Portable and Dockerized: Runs on any Linux/amd64 environment without external dependencies

---

## 📁 Folder Structure

Challenge_1a/  
├── Dockerfile                   # Docker container configuration  
├── process_pdfs.py             # Core PDF outline processing engine  
├── README.md                   # Documentation (this file)  
├── sample_dataset/  
│   ├── pdfs/                   # Input PDF files  
│   ├── outputs/                # JSON output files  
│   └── schema/  
│       └── output_schema.json  # Required JSON output schema

---

## 🛠️ Technologies Used

- Language: Python 3.10  
- PDF Processing: Custom-built logic for analyzing document layout and structure  
- Output: JSON-based structured representation of document outlines  
- Environment: Docker (Linux/amd64, CPU-only)

---

## 🚀 Setup and Usage

### 1️⃣ Build the Docker Image

Open a terminal in the root folder (Challenge_1a/) and run:

docker build --platform linux/amd64 -t pdf-outline-extractor .

---

### 2️⃣ Run the Processor

Use the following command to process your PDFs and generate JSON output:

**Windows PowerShell:**

docker run --rm `  
  -v "${PWD}\sample_dataset\pdfs:/app/input:ro" `  
  -v "${PWD}\sample_dataset\outputs:/app/output" `  
  --network none pdf-outline-extractor

**Linux/macOS:**

docker run --rm \  
  -v "$(pwd)/sample_dataset/pdfs:/app/input:ro" \  
  -v "$(pwd)/sample_dataset/outputs:/app/output" \  
  --network none pdf-outline-extractor

---

### 3️⃣ Output

For each filename.pdf in the /pdfs/ folder, the processor will generate filename.json in the /outputs/ directory. Each output file strictly follows the schema defined in /schema/output_schema.json.

---

## ✅ Constraints Compliance

| Requirement                       | Status            |
|----------------------------------|-------------------|
| Execution ≤ 10 seconds (50 pages)| ✅ Met             |
| Model size ≤ 200MB               | ✅ Lightweight     |
| Internet access disabled         | ✅ Fully offline   |
| CPU-only (no GPU)                | ✅ CPU-efficient   |
| AMD64 Architecture               | ✅ Compatible      |
| Schema-compliant JSON output     | ✅ Fully validated |
| Open Source Tools Only           | ✅ Maintained      |

---

## 📦 Sample Output Format

Each JSON file has the structure:

{
  "title": "Understanding European History",
  "headings": [
    {
      "heading": "Introduction",
      "level": "H1"
    },
    {
      "heading": "Renaissance Period",
      "level": "H2"
    },
    {
      "heading": "Key Artists",
      "level": "H3"
    }
  ]
}

---

## 🧪 Testing Strategy

- PDFs of varying length and complexity were used  
- Included documents with clean text and multi-column formats  
- Validated output using output_schema.json  
- Benchmarked runtime performance on 50-page samples

---

## 📌 Notes

This engine has been designed with adaptability in mind — it can be easily extended to extract deeper heading levels (H4, H5) or integrate layout-aware NLP for semantic tagging.

---

## 📃 License

This project is open-source and licensed under the MIT License.
