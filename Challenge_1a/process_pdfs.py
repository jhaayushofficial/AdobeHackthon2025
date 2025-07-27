# process_pdfs.py
import fitz  # PyMuPDF
import os
import json
from pathlib import Path

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []

    # Step 1: Get title (largest text on page 1)
    page1 = doc[0]
    blocks = page1.get_text("dict")["blocks"]
    max_size = 0
    title = "Untitled"
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span["size"] > max_size:
                    max_size = span["size"]
                    title = span["text"]

    # Step 2: Find headings across pages
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = span["size"]

                    if not text or len(text) < 3 or len(text) > 100:
                        continue

                    # Simple rule-based heading detection
                    if size >= 16:
                        level = "H1"
                    elif size >= 13:
                        level = "H2"
                    elif size >= 11:
                        level = "H3"
                    else:
                        continue

                    outline.append({
                        "level": level,
                        "text": text,
                        "page": page_num
                    })

    return {
        "title": title.strip(),
        "outline": outline
    }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        data = extract_outline(pdf_file)
        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    process_pdfs()
