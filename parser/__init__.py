#!/usr/bin/env python3
"""Select text extractor based on file type"""
import os
from parser import pdf, pptx, docs


def get_extractor(filename: str):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} does not exist")

    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return pdf.extract_text
    elif ext in (".docx", ".doc"):
        return docs.extract_text
    elif ext in (".pptx", ".ppt"):
        return pptx.extract_text
    else:
        raise ValueError(f"Unsupported file type: {ext}")
