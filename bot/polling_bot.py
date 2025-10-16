#!/usr/bin/env python3
"""Entry point into the bot"""

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from bot.utils.env import BOT_TOKEN
from bot.handlers.start import start_handler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

VISION_TEXT = """
*PHILLIP Vision:*
To create a seamless AI-assisted medical learning experience that integrates automation, analytics, and efficiency. 🚀
"""

async def vision_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(VISION_TEXT, parse_mode='Markdown')


async def file_handler(update, context):
    topic = ""
    if update.message.is_topic_message:
        topic = update.message.reply_to_message.forum_topic_created.name
    import json
    print(json.dumps(update.to_dict(), indent=2))
    print(topic)


application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(start_handler)
application.add_handler(CommandHandler('vision', vision_handler))
application.add_handler(MessageHandler(filters.Document.ALL, file_handler))


if __name__ == "__main__":
    print("Bot is running...")
    application.run_polling()
