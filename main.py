#!/usr/bin/env python3
"""Entry point into the bot"""

import asyncio
import logging
from flask import Flask, Response, make_response, request
from http import HTTPStatus
from asgiref.wsgi import WsgiToAsgi
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import uvicorn
from dotenv import load_dotenv

from bot.utils.env import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT
from bot.handlers.start import start_handler
from bot.handlers.group import chat_member_handler, list_groups, select_group
from bot.handlers.unknown import unknown_handler
from bot.handlers.persistence import persistence
from bot.handlers.topic import topic_handler
from bot.handlers.update_handler import update_handler
from bot.handlers.file_handler import file_handler


load_dotenv()

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


application = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence).build()

application.add_handler(start_handler)
application.add_handler(chat_member_handler)
application.add_handler(list_groups)
application.add_handler(select_group)
application.add_handler(CommandHandler('vision', vision_handler))
application.add_handler(topic_handler)
application.add_handler(MessageHandler(filters.Document.ALL, file_handler))
application.add_handler(unknown_handler)
application.add_handler(update_handler)

flask_app = Flask(__name__)

@flask_app.post("/telegram")
async def telegram():
    await application.update_queue.put(Update.de_json(data=request.json, bot=application.bot))
    return Response(status=HTTPStatus.OK)

@flask_app.get("/healthcheck")
async def healthcheck():
    return make_response("✅ Bot is alive and kicking", HTTPStatus.OK)

async def main():
    await application.bot.set_webhook(
        url=f"{WEBHOOK_URL}/telegram",
        allowed_updates=Update.ALL_TYPES,
    )
    server = uvicorn.Server(
        config=uvicorn.Config(app=WsgiToAsgi(flask_app), host="0.0.0.0", port=WEBHOOK_PORT)
    )
    async with application:
        await application.start()
        await server.serve()
        await application.stop()

if __name__ == "__main__":
    asyncio.run(main())
