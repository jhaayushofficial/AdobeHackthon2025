# Adobe India Hackathon 2025 – Challenge 1A & 1B  
**Team Submission: PDF Intelligence Solutions**

---

## 📦 Overview

This repository presents end-to-end solutions for **Challenge 1A** and **Challenge 1B** of the Adobe India Hackathon 2025. The goal was to engineer robust, intelligent, and scalable document processing systems using open technologies and containerized workflows.

Each solution is independently dockerized, fully offline-compatible, and adheres to all execution and performance constraints outlined in the official challenge document.

---

## 🚀 Repository Structure

```
Adobe-India-Hackathon25/
├── Challenge_1a/         # PDF Outline Extraction
│   ├── process_pdfs.py
│   ├── Dockerfile
│   ├── sample_dataset/
│   ├── README.md
│   └── approach_explanation.md
├── Challenge_1b/         # Contextual Section Recommender
│   ├── process_documents.py
│   ├── Dockerfile
│   ├── Collection 1/
│   ├── Collection 2/
│   ├── Collection 3/
│   ├── README.md
│   └── approach_explanation.md
└── .gitignore
```

---

## 📘 Challenge 1A: PDF Outline Extraction

This module extracts the **title**, and hierarchical **headings (H1, H2, H3)** from input PDFs and generates schema-compliant JSON files. It includes:
- Automated batch PDF scanning
- Structural hierarchy detection
- JSON schema validation
- Dockerized for CPU-only execution

📄 Refer to `Challenge_1a/README.md` for full setup and usage.

---

## 📙 Challenge 1B: Persona-Based Section Extraction

This system reads a **persona and job description** from an input config file and analyzes a collection of domain-specific PDFs to extract the **top 5 most relevant document sections** with contextual summaries.

Key features include:
- Persona-aware scoring mechanism
- Page-level section filtering
- Metadata-enhanced summaries (section title, page number, document name)

📄 Refer to `Challenge_1b/README.md` for build and run instructions.

---

## 🧱 Technology Stack

- Python 3.10
- Custom parsing, rule-based logic, and layout analysis
- Docker (Linux/amd64)
- JSON Schema validation
- Fully offline, CPU-only runtime

---

## ✅ Compliance Checklist

| Constraint                                 | Status       |
|-------------------------------------------|--------------|
| Fully offline (no internet access)        | ✅ Met        |
| ≤ 10s execution time (50-page PDFs)       | ✅ Met        |
| ≤ 200MB total image/model size            | ✅ Met        |
| CPU-only (no GPU used)                    | ✅ Met        |
| AMD64 architecture compatible             | ✅ Met        |
| JSON schema conformity                     | ✅ Met        |
| Open-source tools only                    | ✅ Met        |
| Structured documentation                  | ✅ Included   |
| Dockerized solutions (1A & 1B)            | ✅ Both done  |

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Acknowledgments

Special thanks to the Adobe Hackathon team for the opportunity to build and demonstrate innovative document intelligence solutions. This repository reflects a scratch-built, modular, and extensible system designed for real-world PDF analysis and interpretation.

---
