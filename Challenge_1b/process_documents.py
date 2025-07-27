import os
import sys
import fitz  # PyMuPDF
import json
from pathlib import Path
from datetime import datetime

def load_input(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_text_from_pdfs(pdf_dir):
    extracted = []
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            doc_path = os.path.join(pdf_dir, filename)
            doc = fitz.open(doc_path)
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                extracted.append({
                    "document": filename,
                    "page": page_num,
                    "text": text
                })
    return extracted

def score_text(text, keywords):
    score = 0
    for kw in keywords:
        if kw.lower() in text.lower():
            score += 1
    return score

def process(collection_path):
    input_file = os.path.join(collection_path, "challenge1b_input.json")
    output_file = os.path.join(collection_path, "challenge1b_output.json")
    pdf_dir = os.path.join(collection_path, "PDFs")

    if not os.path.exists(input_file):
        print(f"Input JSON not found: {input_file}")
        return
    if not os.path.exists(pdf_dir):
        print(f"PDF folder not found: {pdf_dir}")
        return

    input_data = load_input(input_file)
    persona = input_data["persona"]
    job = input_data["job"]
    keywords = job.lower().split()

    raw_sections = extract_text_from_pdfs(pdf_dir)

    for section in raw_sections:
        section["score"] = score_text(section["text"], keywords)

    sorted_sections = sorted(raw_sections, key=lambda x: x["score"], reverse=True)
    top_sections = sorted_sections[:5]

    output = {
        "metadata": {
            "documents": list(set(s["document"] for s in top_sections)),
            "persona": persona,
            "job": job,
            "timestamp": datetime.now().isoformat()
        },
        "sections": [],
        "subsections": []
    }

    for rank, sec in enumerate(top_sections, start=1):
        output["sections"].append({
            "document": sec["document"],
            "page": sec["page"],
            "section_title": f"Page {sec['page']} - {sec['document']}",
            "importance_rank": rank
        })
        output["subsections"].append({
            "document": sec["document"],
            "page": sec["page"],
            "refined_text": sec["text"].strip().split("\n")[0][:300],
            "importance_rank": rank
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"✅ Output written to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python process_documents.py <collection_folder>")
    else:
        collection_folder = sys.argv[1]
        process(collection_folder)
