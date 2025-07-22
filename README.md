# Round 1a – PDF Outline Extraction

# Overview-
This solution is built for Adobe Hackathon 2025 Round 1A. The task is to extract structured document outlines from PDFs — including title, hierarchical headings (H1, H2, H3), and associated page numbers — and return the result in a well-formatted JSON.

# Our Approach-
We adopted a fast, rule-based logic using text position and font size analysis to approximate structure, while avoiding the need for large ML models. Here's the step-by-step pipeline:

# 1. Title Extraction:
   - The first page is scanned.
   - The longest text span with the largest font size is treated as the title.

# 2. Heading Level Detection:
   - Font sizes are collected across all text spans.
   - The top 3 most frequent large font sizes are mapped to H1, H2, and H3.
   - Any text using these sizes is classified as a heading.

# 3. Outline Construction:
   - Headings are saved with their level, text, and page number.
   - The result is structured as:
     - `"title"`: string
     - `"outline"`: list of heading objects (level, text, page)

# 4. Bonus Feature: Language Support
   - We integrated langdetect to support non-English PDFs.
   - The font-size-based logic works across languages without change.

# Libraries & Tools Used-

| Tool/Library      | Purpose                           |
|------------------|------------------------------------|
| PyMuPDF (fitz)    | PDF parsing and font-size reading |
| langdetect        | Language detection (bonus)        |
| collections.Counter | Font frequency analysis         |
| Docker            | Containerization                  |

# Folder Structure – Round 1A

```bash
adobe_hack_1a/
├── Dockerfile             # Docker container configuration
├── extract_outline.py     # Main script to extract outline from PDFs
├── requirements.txt       # Python dependencies
├── input/                 # Folder containing input PDF files
├── output/                # Folder containing generated output JSONs
└── README.md              # Documentation explaining your approach
```

# How to Build and Run-
Ensure Docker is installed and running.

# Build Docker Image-
docker build -t pdf-outline-extractor .

# Run the Container-
```bash
docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" --network none pdf-outline-extractor
```
🔹 All PDF files in the input folder will be processed.  
🔹 For each PDF, a corresponding `.json` file will be saved in the output folder.

# Example Output-
```bash
{
  "title": "Adobe Marketing Guide 2025",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Campaign Strategy", "page": 2 },
    { "level": "H3", "text": "Social Media Results", "page": 3 }
  ]
}
```

# Key Highlights-
🔹 Works offline — no internet or APIs needed.

🔹 Handles multilingual PDFs.

🔹 Executes in under 10 seconds for large PDFs.

🔹 Outputs consistent JSON format.

🔹 Dockerized for portability across machines.

