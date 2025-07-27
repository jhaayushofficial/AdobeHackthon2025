**[TEAM PHOENIX]**
Team Leader: Arsh Chaudhary
Team Member-1: Anushka Mittal
Team Member-2: Mishthi Goel 



# Adobe Hackathon 2025 – Challenge 1B  
## Intelligent Document Analysis Engine

This project is a fully containerized document intelligence solution developed for Challenge 1B of the Adobe India Hackathon 2025. It processes collections of PDFs and identifies the most relevant sections based on a target user's persona and job role.

## Objective

Given a persona and job title, extract the top 5 most relevant sections from a collection of unstructured PDF documents. The system simulates how a human would browse and filter documents for meaningful insights.

## Features

- Custom PDF parsing and section identification
- Context-aware scoring engine based on persona/job input
- Output in structured JSON format
- Dockerized, portable, and CPU-only (no internet or GPU required)

## Tech Stack

- Python 3.10
- Docker (Linux/amd64)
- PyMuPDF (for text extraction)

## Folder Structure

Challenge_1b/  
├── Dockerfile  
├── process_documents.py  
├── approach_explanation.md  
├── Collection 1/  
│   ├── PDFs/  
│   ├── challenge1b_input.json  
│   └── challenge1b_output.json  
├── Collection 2/  
│   ├── PDFs/  
│   ├── challenge1b_input.json  
│   └── challenge1b_output.json  
├── Collection 3/  
│   ├── PDFs/  
│   ├── challenge1b_input.json  
│   └── challenge1b_output.json  

## How to Use

Step 1: Build the Docker Image  
Open a terminal in the `Challenge_1b` folder and run:

docker build --platform linux/amd64 -t adobe-doc-intel .

This will create a Docker image named `adobe-doc-intel`.

Step 2: Run the Container  
To process a collection (e.g., Collection 1), run:

Windows PowerShell:

docker run --rm -v "${PWD}\Collection 1:/app/input" --network none adobe-doc-intel

Linux / macOS:

docker run --rm -v "$(pwd)/Collection 1:/app/input" --network none adobe-doc-intel

Replace `Collection 1` with `Collection 2` or `Collection 3` to process other datasets.

Step 3: Check Output  
After running the command, check the respective folder for a file named:

challenge1b_output.json

This file contains metadata and the top 5 extracted sections.

## Input Format

Each collection must contain:
- PDFs/: Folder with all PDF files
- challenge1b_input.json: Defines the persona and job

Example input:

{
  "persona": "Frequent Solo Traveler",
  "job": "Travel Content Creator"
}

## Output Format

The output file `challenge1b_output.json` will be structured as:

{
  "persona": "Frequent Solo Traveler",
  "job": "Travel Content Creator",
  "top_sections": [
    {
      "document": "europe_guide.pdf",
      "page": 3,
      "title": "Backpacking Essentials",
      "summary": "Overview of lightweight gear for solo travel."
    }
  ]
}

## Key Constraints Satisfied

- Fully offline (no internet access required)
- CPU-only; no GPU dependencies
- Dockerized and architecture-agnostic (Linux/amd64)
- Uses only open-source libraries
- Runtime under 10 seconds for standard input sets
- Output matches the required schema

## Notes

This implementation demonstrates a complete pipeline for document filtering and summarization based on user-specific roles. It is modular and easy to adapt for advanced semantic techniques.

## 📝 License

This project is licensed under the [MIT License](LICENSE).