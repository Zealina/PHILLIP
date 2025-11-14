#!/usr/bin/env python3
"""Generate AI MCQs with Gemini"""
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, RootModel
from dotenv import load_dotenv
from typing import List


load_dotenv()


class QuestionSchema(BaseModel):
    question: str 
    options: List[str] 
    correct_option: int 
    explanation: str 

class QuestionListSchema(RootModel[List[QuestionSchema]]):
    pass

client = genai.Client()


async def generate_mcqs(text: str, topic: str, per_chunk: int) -> list[dict]:
    """Async generator for MCQs from a given text"""
    topic_text = f"Topic: {topic}"
    prompt = f"""
    Generate {per_chunk} mcqs to test the understanding of resident doctors
    {topic_text if topic else ""}
    Document_Chunk: {text}

    Guidelines:
    - correct_options must use zero-based indexing
    - Ensure the questions are shorter than 250 characters
    - Be creative as a standard body of exam like USMLE, PLAB, NCLEX
    - Add your own twist to the questions based on your knowledge of the topic
    - Ask questions to cover blind spots in the document as well
    - Every explanation must include the page number, for reference
    - If the chunk lacks enough context, return empty list.
    """
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=QuestionListSchema,
            temperature=0.8
        )
    )

    return json.loads(response.text)
