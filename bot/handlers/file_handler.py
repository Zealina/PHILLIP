"""Handle Uploaded files"""
import asyncio
import os
from telegram import Update, Poll
from telegram.ext import ContextTypes
from ai_questioner.generate import run_generator
from werkzeug.utils import secure_filename


UPLOAD_DIR = "uploads/"


async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert document files e.g .pdf, .pptx, .docx to questions"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    unsafe_name = update.message.document.file_name
    safe_name = secure_filename(unsafe_name)
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    tg_file = await context.bot.get_file(update.message.document.file_id)
    await tg_file.download_to_drive(custom_path=file_path)

    async for result in run_generator(file_path):
        for entry in result:
            try:
                await update.message.reply_poll(
                    question=entry.get("question"),
                    options=entry.get("options"),
                    type=Poll.QUIZ,
                    correct_option_id=entry.get("correct_option"),
                    explanation=entry.get("explanation")
                )
            except Exception as e:
                pass
            await asyncio.sleep(2.1)
