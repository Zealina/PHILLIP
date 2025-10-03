#!/usr/bin/env python3
"""
Convert a .docx file to .txt while preserving original structure.
Tables appear where they are in the document flow.
"""

import os
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


def docx_to_txt(docx_path):
    if not docx_path.lower().endswith('.docx'):
        raise ValueError("Only .docx files are supported.")

    doc = Document(docx_path)
    base_name = os.path.splitext(os.path.basename(docx_path))[0]
    output_file = f"{base_name}.txt"

    with open(output_file, "w", encoding="utf-8") as out:
        for block in iter_block_items(doc):
            if isinstance(block, Paragraph):
                text = block.text.strip()
                if text:
                    out.write(text + "\n")
            elif isinstance(block, Table):
                for row in block.rows:
                    row_data = [cell.text.strip() for cell in row.cells]
                    out.write(" | ".join(row_data) + "\n")
                out.write("\n")  # spacing between tables/next paragraph

    print(f"Conversion complete: {output_file}")


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: ./docx_to_txt.py <your_file.docx>")
        exit(1)

    docx_to_txt(argv[1])
