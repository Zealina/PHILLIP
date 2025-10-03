#!/usr/bin/env python3
"""
Convert a .pptx PowerPoint file to a .txt file.
Preserves the order of content: titles, paragraphs, and tables.
"""

import os
from sys import argv
from pptx import Presentation


def extract_table(table):
    """Return table text as list of rows (strings)."""
    rows = []
    for row in table.rows:
        cell_texts = [cell.text.strip() for cell in row.cells]
        rows.append(" | ".join(cell_texts))
    return rows


def pptx_to_txt(pptx_path):
    if not pptx_path.lower().endswith(".pptx"):
        raise ValueError("Only .pptx files are supported.")

    prs = Presentation(pptx_path)
    base_name = os.path.splitext(os.path.basename(pptx_path))[0]
    output_file = f"{base_name}.txt"

    with open(output_file, "w", encoding="utf-8") as out:
        for slide_num, slide in enumerate(prs.slides, start=1):
            out.write(f"\n--- Slide {slide_num} ---\n\n")

            for shape in slide.shapes:
                if not shape.has_text_frame and not shape.has_table:
                    continue

                # Text (titles, bullets, etc.)
                if shape.has_text_frame:
                    for para in shape.text_frame.paragraphs:
                        text = para.text.strip()
                        if text:
                            out.write(text + "\n")

                # Table
                if shape.has_table:
                    table = shape.table
                    table_text = extract_table(table)
                    for row in table_text:
                        out.write(row + "\n")
                    out.write("\n")

    print(f"Conversion complete: {output_file}")


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: ./pptx_to_txt.py <your_file.pptx>")
        exit(1)

    pptx_to_txt(argv[1])

