#!/usr/bin/env python3
"""Extract text from a .docx document in natural reading order"""
import re
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from sys import argv


def iter_block_items(parent):
    """
    Yield paragraphs and tables in the order they appear in the document.
    """
    for child in parent.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

def extract_text(docx_path, chunksize: int = 200):
    """Yield text chunks from a .docx file"""
    if not docx_path.lower().endswith(".docx"):
        raise ValueError("Input file must be a .docx file")

    doc = Document(docx_path)
    buffer = []
    word_count = 0

    sentence_splitter = re.compile(r"(?<=[.!?])\s+")

    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if not text:
                continue

            sentences = sentence_splitter.split(text)
            for sentence in sentences:
                words = sentence.split()
                if not words:
                    continue

                if word_count + len(words) > chunksize:
                    chunk = " ".join(buffer).strip()
                    if chunk:
                        yield f"{chunk})"
                    buffer = []
                    word_count = 0

                buffer.extend(words)
                word_count += len(words)

        elif isinstance(block, Table):
            for row in block.rows:
                row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if not row_data:
                    continue
                line = " | ".join(row_data)
                words = line.split()

                if word_count + len(words) > chunksize:
                    chunk = " ".join(buffer).strip()
                    if chunk:
                        yield f"{chunk}"
                    buffer = []
                    word_count = 0

                buffer.extend(words)
                word_count += len(words)

    if buffer:
        chunk = " ".join(buffer).strip()
        if chunk:
            yield f"{chunk}\n\n[End of document]"
