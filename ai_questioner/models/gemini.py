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


async def generate_mcqs(text: str, topic: str) -> list[dict]:
    """Async generator for MCQs from a given text"""
    prompt = f"""
    You are a medical exam question generator.
    Below is a document chunk extracted from a lecture note.

    Topic: {topic}
    Document_Chunk: ...{text}

    Your task:
    - Generate 2 multiple-choice questions (MCQs) in valid JSON format only.

    Guidelines:
    - Ensure the questions are shorter than 250 characters
    - Try to avoid "which of the following..." and "What.." questions
    - Every explanation must include the page number where the information came from
    - Ensure all questions are factually derived from the chunk.
    - If the chunk contains irrelevant content (e.g., references, acknowledgments, Title page) return empty list .
    - If the chunk is too short or lacks enough context, return empty list.
    """

    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=QuestionListSchema,
            temperature=0.7
        )
    )

    return json.loads(response.text)
