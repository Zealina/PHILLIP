#!/usr/bin/env python3
"""Read the file and generate the questions from AI"""
import asyncio
import random
from parser import get_extractor
from ai_questioner.models import gemini
from typing import Dict


LIMIT = 10


async def run_generator(filename: str):
    """Get the questions from the API"""
    extractor = get_extractor(filename)
    all_tasks = [gemini.generate_mcqs(chunk) for chunk in extractor(filename)]

    i = 0
    while i < len(all_tasks):
        tasks = all_tasks[i : i + LIMIT]
        i += LIMIT
        for coro in asyncio.as_completed(tasks):
            result = await coro
            result = [randomize_options(entry) for entry in result]
            yield result
        await asyncio.sleep(61)


def randomize_options(data: Dict):
    """Randomize the options in the dictionary"""
    if not data.get("options"):
        raise ValueError("No OPTIONS in data")
    if not data.get("correct_option"):
        raise ValueError("Correct OPTION is not set")

    correct_option = data["options"][data["correct_option"]]
    random.shuffle(data["options"])
    data["correct_option"] = data["options"].index(correct_option)
    return data
