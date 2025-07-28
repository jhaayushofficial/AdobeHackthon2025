# process_pdfs.py
import fitz  # PyMuPDF
import os
import json
import re
from pathlib import Path

def is_valid_heading(text, size, position_y):
    """Validate if text is likely a heading based on multiple criteria"""
    text = text.strip()
    
    # Basic length validation
    if len(text) < 3 or len(text) > 200:
        return False
    
    # Skip common non-heading patterns
    non_heading_patterns = [
        r'^\d+$',  # Just numbers
        r'^[a-z]+\s*$',  # Just lowercase words
        r'^\s*[.,;:!?]+\s*$',  # Just punctuation
        r'^\s*$',  # Empty or whitespace
        r'^[A-Za-z]\s*$',  # Single character
    ]
    
    for pattern in non_heading_patterns:
        if re.match(pattern, text):
            return False
    
    # Check for heading-like characteristics
    has_heading_characteristics = (
        # Starts with capital letter or number
        (text[0].isupper() or text[0].isdigit()) and
        # Contains meaningful content (not just punctuation)
        len(re.sub(r'[^\w\s]', '', text)) > 2 and
        # Not too many special characters
        len(re.findall(r'[^\w\s]', text)) < len(text) * 0.3
    )
    
    return has_heading_characteristics

def extract_title(page1):
    """Extract title from the first page with robust logic for Adobe.pdf"""
    blocks = page1.get_text("dict")["blocks"]
    candidates = []
    
    # Debug: Print all text found on first page
    print("DEBUG: All text found on first page:")
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                size = span["size"]
                if text and len(text) > 2:
                    print(f"  Text: '{text}' (size: {size})")
    
    # Strategy 1: Look for large, prominent text (most likely titles)
    for block in blocks:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span["text"].strip()
                size = span["size"]
                bbox = span.get("bbox", [0, 0, 0, 0])
                
                if not text or len(text) < 2:
                    continue
                
                # Skip obvious non-titles
                if (text.isdigit() or 
                    text.lower() in ['page', 'contents', 'index', 'appendix', 'copyright'] or
                    len(text) > 200):
                    continue
                
                # Score based on multiple criteria
                score = 0
                
                # Large font gets high score
                if size >= 16:
                    score += 10
                elif size >= 14:
                    score += 8
                elif size >= 12:
                    score += 5
                
                # Position matters (top of page = higher score)
                position_score = 1.0 - (bbox[1] / page1.rect.height)
                score += position_score * 5
                
                # ALL CAPS gets bonus
                if text.isupper() and 3 <= len(text) <= 100:
                    score += 3
                
                # Title case gets bonus
                if text[0].isupper() and len(re.sub(r'[^\w\s]', '', text)) > 3:
                    score += 2
                
                # Common title words get bonus
                title_words = ['welcome', 'introduction', 'overview', 'about', 'challenge', 'connecting', 'dots']
                if any(word in text.lower() for word in title_words):
                    score += 4
                
                if score > 5:  # Only consider candidates with decent score
                    candidates.append((text, score, size, bbox[1]))
                    print(f"DEBUG: Candidate '{text}' (score: {score}, size: {size})")
    
    # Strategy 2: If no good candidates, look for any meaningful text
    if not candidates:
        print("DEBUG: No good candidates found, trying strategy 2")
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    size = span["size"]
                    bbox = span.get("bbox", [0, 0, 0, 0])
                    
                    if (text and len(text) > 5 and len(text) < 150 and 
                        text[0].isupper() and not text.isdigit()):
                        position_score = 1.0 - (bbox[1] / page1.rect.height)
                        candidates.append((text, position_score * 3, size, bbox[1]))
                        print(f"DEBUG: Strategy 2 candidate '{text}' (score: {position_score * 3})")
    
    # Strategy 3: Last resort - use first meaningful text
    if not candidates:
        print("DEBUG: No candidates found, using strategy 3")
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text and len(text) > 10 and len(text) < 100:
                        print(f"DEBUG: Strategy 3 found '{text}'")
                        return text
    
    # Sort by score (highest first), then by position (top first)
    candidates.sort(key=lambda x: (-x[1], x[3]))
    
    # Return the best candidate
    if candidates:
        print(f"DEBUG: Best candidate: '{candidates[0][0]}' (score: {candidates[0][1]})")
        return candidates[0][0]
    else:
        print("DEBUG: No candidates found, returning default")
        return "Document Title"

def determine_heading_level(size, text, position_y, page_height):
    """Determine heading level using multiple criteria, not just font size"""
    text = text.strip()
    
    # Base level on font size
    if size >= 16:
        base_level = "H1"
    elif size >= 13:
        base_level = "H2"
    elif size >= 11:
        base_level = "H3"
    else:
        return None
    
    # Adjust based on position (top of page = higher level)
    relative_position = position_y / page_height
    if relative_position < 0.2:  # Top 20% of page
        if base_level == "H2":
            base_level = "H1"
        elif base_level == "H3":
            base_level = "H2"
    
    # Adjust based on text characteristics
    if text.isupper() and len(text) < 50:  # ALL CAPS short text
        if base_level == "H2":
            base_level = "H1"
        elif base_level == "H3":
            base_level = "H2"
    
    return base_level

def merge_adjacent_text(spans):
    """Merge adjacent text spans that belong to the same heading"""
    if not spans:
        return []
    
    merged = []
    current_text = ""
    current_size = spans[0]["size"]
    current_bbox = spans[0].get("bbox", [0, 0, 0, 0])
    
    for span in spans:
        text = span["text"].strip()
        size = span["size"]
        bbox = span.get("bbox", [0, 0, 0, 0])
        
        # If same size and close position, merge
        if (abs(size - current_size) < 2 and 
            abs(bbox[1] - current_bbox[1]) < 5):
            current_text += " " + text if current_text else text
        else:
            # Save previous merged text
            if current_text:
                merged.append({
                    "text": current_text.strip(),
                    "size": current_size,
                    "bbox": current_bbox
                })
            # Start new text
            current_text = text
            current_size = size
            current_bbox = bbox
    
    # Add the last merged text
    if current_text:
        merged.append({
            "text": current_text.strip(),
            "size": current_size,
            "bbox": current_bbox
        })
    
    return merged

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []
    
    # Step 1: Extract title with robust logic
    page1 = doc[0]
    title = extract_title(page1)
    
    # If title is still "Document Title", try to get it from the first meaningful heading
    if title == "Document Title":
        print("DEBUG: Title extraction failed, trying to get title from first heading")
        for page_num, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span["text"].strip()
                        size = span["size"]
                        
                        if (text and len(text) > 5 and len(text) < 100 and 
                            text[0].isupper() and size >= 12):
                            print(f"DEBUG: Using first heading as title: '{text}'")
                            title = text
                            break
                    if title != "Document Title":
                        break
                if title != "Document Title":
                    break
            if title != "Document Title":
                break
    
    # Step 2: Find headings across pages with better detection
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        page_height = page.rect.height
        
        # Collect all text spans on this page
        page_spans = []
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text:
                        page_spans.append(span)
        
        # Merge adjacent text spans
        merged_spans = merge_adjacent_text(page_spans)
        
        # Process merged spans as potential headings
        for span in merged_spans:
            text = span["text"]
            size = span["size"]
            bbox = span["bbox"]
            position_y = bbox[1] if bbox else 0
            
            # Validate if this is a heading
            if not is_valid_heading(text, size, position_y):
                continue
            
            # Determine heading level
            level = determine_heading_level(size, text, position_y, page_height)
            if not level:
                continue
            
            outline.append({
                "level": level,
                "text": text,
                "page": page_num
            })
    
    return {
        "title": title,
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
