import os
import sys
import fitz  # PyMuPDF
import json
import re
from pathlib import Path
from datetime import datetime

def load_input(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_proper_headings(page):
    """Extract proper section headings using advanced layout analysis"""
    blocks = page.get_text("dict")["blocks"]
    headings = []
    
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                size = span["size"]
                
                if not text or len(text) < 3:
                    continue
                
                # Advanced heading detection
                is_heading = (
                    # Large font size
                    size >= 16 or
                    # ALL CAPS with reasonable length
                    (text.isupper() and 3 <= len(text) <= 100) or
                    # Numbered sections (1. Title, 1.1 Subtitle, etc.)
                    re.match(r'^\d+\.?\d*\s+[A-Z]', text) or
                    # Title case with reasonable length
                    (re.match(r'^[A-Z][a-z]+', text) and len(text) <= 80) or
                    # Recipe-style headings
                    re.match(r'^[A-Z][a-z\s]+(Recipe|Dinner|Meal|Cooking|Kitchen)', text, re.IGNORECASE)
                )
                
                # Filter out common non-headings
                if is_heading and not any(skip in text.lower() for skip in ['page', 'contents', 'index', 'appendix', 'copyright']):
                    headings.append({
                        "text": text,
                        "size": size,
                        "bbox": span.get("bbox", [0, 0, 0, 0])
                    })
    
    return headings

def extract_complete_sections(pdf_path):
    """Extract complete, coherent sections with proper titles"""
    doc = fitz.open(pdf_path)
    sections = []
    
    for page_num, page in enumerate(doc, start=1):
        # Get proper headings first
        headings = extract_proper_headings(page)
        
        # Get all text blocks for content
        blocks = page.get_text("dict")["blocks"]
        page_text = ""
        
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text and len(text) > 1:
                        page_text += " " + text
        
        page_text = re.sub(r'\s+', ' ', page_text).strip()
        
        # Create sections based on headings
        if headings:
            for heading in headings:
                # Find content after this heading
                heading_pos = page_text.find(heading["text"])
                if heading_pos != -1:
                    # Get content after heading (up to next heading or end)
                    content_start = heading_pos + len(heading["text"])
                    content = page_text[content_start:].strip()
                    
                    # Clean up content
                    content = re.sub(r'^\s*[.,;:]\s*', '', content)
                    
                    if content and len(content) > 20:
                        sections.append({
                            "page": page_num,
                            "title": heading["text"],
                            "content": content,
                            "font_size": heading["size"]
                        })
        else:
            # If no headings found, create sections from paragraphs
            paragraphs = [p.strip() for p in page_text.split('\n') if len(p.strip()) > 50]
            for i, para in enumerate(paragraphs[:3]):  # Limit to 3 sections per page
                if para:
                    sections.append({
                        "page": page_num,
                        "title": f"Section {i+1}",
                        "content": para,
                        "font_size": 12
                    })
    
    return sections

def advanced_semantic_scoring(section, persona, job):
    """Advanced semantic scoring with context understanding"""
    text = (section["title"] + " " + section["content"]).lower()
    score = 0
    
    # Enhanced persona-specific keywords with synonyms
    persona_keywords = {
        "home chef": [
            "recipe", "cook", "dinner", "meal", "food", "ingredient", "preparation", 
            "cooking", "kitchen", "chef", "dish", "cuisine", "cookbook", "menu",
            "prep", "bake", "grill", "roast", "simmer", "season", "spice", "herb"
        ],
        "researcher": [
            "research", "study", "analysis", "methodology", "findings", "data", 
            "experiment", "results", "conclusion", "hypothesis", "theory", "evidence",
            "investigation", "observation", "measurement", "statistics"
        ],
        "student": [
            "learn", "study", "education", "course", "lesson", "tutorial", "guide", 
            "instruction", "chapter", "topic", "concept", "principle", "theory",
            "practice", "exercise", "assignment", "review"
        ],
        "investor": [
            "financial", "revenue", "profit", "investment", "market", "growth", 
            "earnings", "stock", "dividend", "portfolio", "return", "valuation",
            "quarterly", "annual", "performance", "strategy"
        ],
        "journalist": [
            "news", "report", "story", "interview", "event", "announcement", 
            "press", "media", "coverage", "breaking", "update", "developing",
            "exclusive", "investigation", "feature"
        ]
    }
    
    # Enhanced job-specific keywords
    job_keywords = {
        "quick dinner": [
            "quick", "fast", "easy", "simple", "30 minute", "weeknight", "dinner", 
            "meal", "recipe", "speedy", "rapid", "hasty", "swift", "prompt",
            "time-saving", "efficient", "convenient", "ready", "prepared"
        ],
        "literature review": [
            "review", "literature", "research", "study", "analysis", "findings", 
            "methodology", "survey", "overview", "summary", "synthesis",
            "meta-analysis", "systematic", "comprehensive"
        ],
        "financial analysis": [
            "financial", "revenue", "profit", "earnings", "growth", "market", 
            "investment", "performance", "quarterly", "annual", "valuation",
            "profitability", "cash flow", "balance sheet", "income statement"
        ],
        "exam preparation": [
            "exam", "test", "study", "review", "practice", "question", "answer", 
            "preparation", "revision", "memorization", "concept", "topic",
            "key points", "important", "essential", "critical"
        ]
    }
    
    # Score based on persona with weighted matching
    persona_lower = persona.lower()
    for key, keywords in persona_keywords.items():
        if key in persona_lower:
            for keyword in keywords:
                if keyword in text:
                    # Weight by keyword importance
                    if keyword in ["recipe", "cook", "dinner", "meal"]:
                        score += 3
                    else:
                        score += 2
    
    # Score based on job with enhanced matching
    job_lower = job.lower()
    for key, keywords in job_keywords.items():
        if key in job_lower:
            for keyword in keywords:
                if keyword in text:
                    # Weight by keyword importance
                    if keyword in ["quick", "fast", "easy", "dinner", "recipe"]:
                        score += 4
                    else:
                        score += 3
    
    # Bonus for content quality
    if len(section["content"]) > 100:
        score += 2
    
    # Bonus for proper headings
    if section["title"] and len(section["title"]) > 3:
        score += 2
    
    # Bonus for cooking-specific terms
    cooking_terms = ["ingredient", "preparation", "cook time", "serves", "prep time"]
    for term in cooking_terms:
        if term in text:
            score += 1
    
    return score

def extract_meaningful_title(section):
    """Extract a meaningful, complete section title"""
    title = section["title"]
    
    # Clean up the title
    title = re.sub(r'^\d+\.?\s*', '', title)  # Remove leading numbers
    title = title.strip()
    
    # If title is too long, truncate intelligently
    if len(title) > 80:
        # Try to find a natural break point
        words = title.split()
        if len(words) > 5:
            title = " ".join(words[:5]) + "..."
    
    # If no meaningful title, create one from content
    if not title or len(title) < 3:
        content = section["content"]
        # Find first meaningful sentence
        sentences = re.split(r'[.!?]', content)
        for sentence in sentences:
            sentence = sentence.strip()
            if 10 < len(sentence) < 100:
                title = sentence
                break
    
    return title if title else f"Section from page {section['page']}"

def extract_complete_refined_text(section):
    """Extract complete, coherent refined text"""
    content = section["content"]
    
    # Clean up content
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    
    # Find complete sentences
    sentences = re.split(r'[.!?]', content)
    complete_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if 20 < len(sentence) < 500:
            complete_sentences.append(sentence)
    
    # Combine sentences up to 300 characters
    result = ""
    for sentence in complete_sentences:
        if len(result + sentence) <= 300:
            result += sentence + ". "
        else:
            break
    
    return result.strip() if result else content[:300]

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

    # Process all PDFs and extract complete sections
    all_sections = []
    documents = []
    
    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            documents.append(filename)
            pdf_path = os.path.join(pdf_dir, filename)
            sections = extract_complete_sections(pdf_path)
            
            for section in sections:
                section["document"] = filename
                section["relevance_score"] = advanced_semantic_scoring(section, persona, job)
                all_sections.append(section)

    # Sort by relevance score and get top 5
    sorted_sections = sorted(all_sections, key=lambda x: x["relevance_score"], reverse=True)
    top_sections = sorted_sections[:5]

    # Generate output
    output = {
        "metadata": {
            "documents": documents,
            "persona": persona,
            "job": job,
            "timestamp": datetime.now().isoformat()
        },
        "sections": [],
        "subsections": []
    }

    for rank, section in enumerate(top_sections, start=1):
        section_title = extract_meaningful_title(section)
        refined_text = extract_complete_refined_text(section)
        
        output["sections"].append({
            "document": section["document"],
            "page": section["page"],
            "section_title": section_title,
            "importance_rank": rank
        })
        
        output["subsections"].append({
            "document": section["document"],
            "page": section["page"],
            "refined_text": refined_text,
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
