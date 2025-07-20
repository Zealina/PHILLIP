import os

from parser.document.pdf_to_txt import pdf_to_txt
from parser.document.docx_to_txt import docx_to_txt
from parser.document.pptx_to_txt import pptx_to_txt


def convert_to_txt(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No such file: {filepath}")

    ext = os.path.splitext(filepath)[-1].lower()
    if ext == ".pdf":
        return pdf_to_txt(filepath)
    elif ext == ".docx":
        return docx_to_txt(filepath)
    elif ext == ".pptx":
        return pptx_to_txt(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

