#!/usr/bin/env python3
"""Entry point into the bot"""

from telegram.ext import ApplicationBuilder
from bot.utils.env import BOT_TOKEN
from bot.handlers.start import start_handler
from bot.handlers.chat_member import chat_member_handler
from bot.handlers.unknown import unknown_handler


application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(start_handler)
application.add_handler(chat_member_handler)
application.add_handler(unknown_handler)


if __name__ == '__main__':
    print("PHILLIP has started...")
    application.run_polling()
