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
    You are a consultant O & G, Generate {per_chunk} mcqs to test the understanding of students
    {topic_text if topic else ""}
    {text}

    Guidelines:
    - correct_options must use zero-based indexing
    - Ensure the questions are shorter than 250 characters
    - Be precise with questions, no adding extra context
    - Ask questions to cover blind spots in the document as well
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
