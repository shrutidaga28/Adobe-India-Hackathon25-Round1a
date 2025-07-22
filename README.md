# Adobe Hackathon - Round 1A: PDF Outline Extractor

## 🚀 Overview
This project is built for Adobe’s “Connecting the Dots” Hackathon Round 1A.  
The tool extracts a **document title** and **outline structure (H1, H2, H3 headings)** from any PDF file and returns a properly formatted `.json`.

---

## 📁 Input/Output Format

- Input: Any `.pdf` file (max 50 pages)
- Output: Corresponding `.json` file in the format:
```json
{
  "title": "Your Document Title",
  "outline": [
    { "level": "H1", "text": "Heading Text", "page": 1 },
    { "level": "H2", "text": "Subheading Text", "page": 2 }
  ]
}
