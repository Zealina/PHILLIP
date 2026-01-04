#!/usr/bin/env python3
"""Read the file and generate the questions from AI"""
import asyncio
import random
from parser import get_extractor
from ai_questioner.models import gemini
from typing import Dict


LIMIT = 4
async def run_generator(filename: str, topic: str, per_page: int):
    """Get the questions from the API"""
    extractor = get_extractor(filename)
    all_tasks = [gemini.generate_mcqs(chunk, topic, per_page) for chunk in extractor(filename)]

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
    if not data or data.get("options") is None:
        return None
    if data.get("correct_option") is None:
        data["correct_option"] = 0

    options = data["options"]
    new_options = []
    for option in options:
        new_options.append(option[:100])
    data["options"] = new_options

    question = data.get("question")
    if question:
        data["question"] = question[:255]

    correct_option = data["options"][data["correct_option"]]
    random.shuffle(data["options"])
    data["correct_option"] = data["options"].index(correct_option)
    return data
