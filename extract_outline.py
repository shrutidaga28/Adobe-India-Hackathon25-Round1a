import fitz  # PyMuPDF
import os
import json
import unicodedata
from langdetect import detect, DetectorFactory
from collections import Counter

# Fix randomness in langdetect
DetectorFactory.seed = 0

# Folder paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Loop through all PDF files in the input folder
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(INPUT_DIR, filename)
        doc = fitz.open(pdf_path)

        # --- Step 1: Extract Title (from first page) ---
        first_page = doc[0]
        title = ""
        max_size = 0

        for block in first_page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        raw_text = span["text"]
                        text = unicodedata.normalize("NFKC", raw_text).strip()
                        size = span["size"]
                        if len(text) > 5 and size > max_size:
                            max_size = size
                            title = text

        # --- Step 2: Analyze font sizes to detect headings ---
        font_sizes = []

        for page in doc:
            for block in page.get_text("dict")["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            font_sizes.append(round(span["size"]))

        # Identify top 3 common largest font sizes
        common_sizes = Counter(font_sizes).most_common()
        top_fonts = [size for size, count in common_sizes[:5]]
        top_fonts.sort(reverse=True)

        if len(top_fonts) < 3:
            print(f"[{filename}] Not enough distinct font sizes found.")
            continue

        font_to_level = {
            top_fonts[0]: "H1",
            top_fonts[1]: "H2",
            top_fonts[2]: "H3"
        }

        # --- Step 3: Extract headings with levels, page numbers & language ---
        outline = []

        for page_number, page in enumerate(doc, start=1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            raw_text = span["text"]
                            text = unicodedata.normalize("NFKC", raw_text).strip()
                            size = round(span["size"])

                            if size in font_to_level and len(text) > 3:
                                try:
                                    language = detect(text)
                                except:
                                    language = "unknown"

                                outline.append({
                                    "level": font_to_level[size],
                                    "text": text,
                                    "page": page_number,
                                    "language": language
                                })

        # --- Step 4: Save the result as JSON ---
        result = {
            "title": title,
            "outline": outline
        }

        output_filename = filename.lower().replace(".pdf", ".json")
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)  # ensure_ascii=False = show native characters

        print(f"✅ Processed: {filename} → {output_filename}")


