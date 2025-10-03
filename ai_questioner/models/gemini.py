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
    options: List
    correct_option: int
    explanation: str


class QuestionListSchema(RootModel[List[QuestionSchema]]):
    pass

client = genai.Client()


async def generate_mcqs(text: str) -> list[dict]:
    """Async generator for MCQs from a given text"""

    prompt = f"""
    Source text: {text}

    Generate 3-5 MCQs in the exact JSON format.
    Tne explanation should have the page number included in it
    The explanation should not be more than 100 characters
    The question should not be more than 255 characters
    The options should each not be more than 100 characters
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
