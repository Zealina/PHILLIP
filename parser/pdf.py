#!/usr/bin/env python3
"""Extract text from a PDF document"""

import pymupdf


def extract_text(pdf_path):
    if not pdf_path.lower().endswith('.pdf'):
        raise ValueError("Input file must be a .pdf file")

    doc = pymupdf.open(pdf_path)
    for page_no, page in enumerate(doc, start=1):
        text = page.get_text("text")
        text += f"\n\nPage: {page_no}"
        print(text)
        yield text
