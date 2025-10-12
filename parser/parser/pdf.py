#!/usr/bin/env python3
"""Extract text from a PDF document"""
import pymupdf
import re


def extract_text(pdf_path, chunk_size=300):
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Input file must be a .pdf file")

    doc = pymupdf.open(pdf_path)
    buffer = []
    word_count = 0

    sentence_splitter = re.compile(r"(?<=[.!?])\s+")

    for page_no, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if not text:
            continue

        sentences = sentence_splitter.split(text)
        page_buffer = []

        for sentence in sentences:
            words_in_sentence = sentence.split()
            if not words_in_sentence:
                continue

            if word_count + len(words_in_sentence) > chunk_size:
                if page_buffer:
                    buffer.extend(page_buffer)
                    page_buffer = []

                chunk = " ".join(buffer).strip()
                if chunk:
                    yield f"{chunk}"

                buffer = []
                word_count = 0
                pages_in_chunk = []

            page_buffer.extend(words_in_sentence)
            word_count += len(words_in_sentence)

        if page_buffer:
            buffer.extend(page_buffer)
            buffer.append(f"\n(Page {page_no})\n")

    if buffer:
        chunk = " ".join(buffer).strip()
        if chunk:
            yield f"{chunk}\n\n[End of document]"
