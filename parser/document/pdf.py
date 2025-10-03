#!/usr/bin/env python3
"""Extract text from a PDF document
Leaves images in-place but manages tables using layout-preserving text extraction.
"""

import pymupdf
from sys import argv
import os

def extract_text(pdf_path):
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("Input file must be a .pdf file")

    doc = pymupdf.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_file = f"{base_name}.txt"

    with open(output_file, "w", encoding="utf-8") as out:
        for i, page in enumerate(doc, start=1):
            out.write(f"\n\n--- Page {i} ---\n\n")
            text = page.get_text("text")
            out.write(text)
    
    print(f"Conversion complete: {output_file}")

if __name__ == "__main__":
    if len(argv) < 2:
        raise ValueError("Usage: ./pdf.py <FILE>")
    
    extract_text(argv[1])

