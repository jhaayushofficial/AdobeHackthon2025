# Approach – Challenge 1B: Intelligent Document Understanding

## 🔍 Problem Understanding

The task required developing an intelligent system that could extract the top 5 most relevant sections from a collection of unstructured PDF documents, based on a given persona and job description. This simulated how a human might filter and absorb critical information tailored to their interests.

## 🧠 Design Philosophy

Our solution focuses on custom document intelligence, integrating text parsing, semantic filtering, and rule-based prioritization to identify content that aligns with the target user's intent. The architecture is modular, efficient, and fully containerized for consistent cross-platform performance.

## 🧱 Architecture Overview

1. **Input Ingestion**  
   Each collection folder includes a persona, job description, and a batch of PDFs. The input JSON is parsed to extract the user’s context.

2. **Document Parsing Engine**  
   A fast and lightweight document parser was built to scan PDFs page by page, segmenting content into sections by recognizing headings, formatting patterns, and layout cues. This parsing layer is built for high efficiency and resilience across document types.

3. **Context-Aware Scoring**  
   A scoring mechanism compares each section against the persona and job using keyword mapping, semantic overlap, and contextual relevance. This helps emulate how a human would assess information importance.

4. **Ranking and Filtering**  
   Sections are scored, ranked, and filtered to identify the most contextually aligned content. The top 5 sections across the document set are selected based on their relevance scores.

5. **Summarization Layer**  
   To improve readability and precision, each section is summarized. The output includes document name, page number, section title, and a brief summary.

6. **JSON Output Generation**  
   The final output is a JSON file that strictly conforms to the challenge schema. This structured output provides clean insights for downstream applications or reporting.

## 🧰 Technologies Used

- Language: Python 3.10  
- Containerization: Docker (Linux/amd64)  
- PDF Processing: Custom logic for parsing and structure segmentation  
- Deployment: CPU-only, no network dependency

## 📦 Dockerization Strategy

To ensure reliability and environment consistency, the complete solution is packaged into a Docker container. Inputs are provided via a mounted volume, and all processing is sandboxed for security and reproducibility.

**Build Command:**
docker build --platform linux/amd64 -t adobe-doc-intel .

**Run Command (for Collection 1):**
docker run --rm -v "${PWD}\Collection 1:/app/input" --network none adobe-doc-intel

Replace `Collection 1` with any other collection folder to test multiple datasets.

## ✅ Constraints Handling

| Constraint                         | Status                              |
|-----------------------------------|-------------------------------------|
| Max Execution Time (≤ 10s)        | ✅ Optimized parsing and logic      |
| Memory Usage (≤ 16GB)             | ✅ Efficient memory handling        |
| CPU-Only, AMD64                   | ✅ Fully supported                  |
| No Internet Access                | ✅ Works 100% offline               |
| Output Schema Compliance          | ✅ Validated and strictly followed  |
| Multi-document & Layout Robustness| ✅ Tested across PDF complexities   |

## 🧪 Testing Strategy

The solution was tested across:
- Simple PDFs (linear text flow)
- PDFs with multiple columns, headings, and diverse formatting
- Different persona/job inputs to validate semantic filtering

Results were evaluated for relevance, speed, and accuracy, ensuring adherence to Adobe’s runtime and output constraints.

## 🧾 Conclusion

The system reflects a real-world, context-sensitive approach to intelligent document extraction. Built with flexibility, performance, and future extensibility in mind, it showcases how persona-driven filtering can significantly improve user experience in document-heavy workflows.
