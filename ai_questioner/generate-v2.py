import asyncio
import random
from parser import get_extractor
from ai_questioner.models import gemini
from typing import Dict, List, Tuple


MODEL_LIMITS = {
    "gemini-2.5-flash": {"rate": 10, "per": 60},
    "gemini-2.0-flash": {"rate": 15, "per": 60},
}

async def run_generator(filename: str):
    """Distribute requests across multiple models respecting rate limits"""
    extractor = get_extractor(filename)
    chunks = list(extractor(filename))

    results: List[Tuple[int, List[Dict]]] = []

    async def limited_generate(chunk, idx, model: str):
        result = await gemini.generate_mcqs(chunk, model=model)
        result = [randomize_options(entry) for entry in result]
        return idx, result

    i = 0
    while i < len(chunks):
        batch_tasks = []
        for model, limits in MODEL_LIMITS.items():
            model_chunks = chunks[i : i + limits["rate"]]
            for j, chunk in enumerate(model_chunks):
                batch_tasks.append(limited_generate(chunk, i + j, model))
            i += len(model_chunks)

            if i >= len(chunks):
                break

        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)

        if i < len(chunks):
            await asyncio.sleep(max(l["per"] for l in MODEL_LIMITS.values()))

    results.sort(key=lambda x: x[0])
    for _, result in results:
        yield result


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

