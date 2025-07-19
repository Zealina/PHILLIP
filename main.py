#!/usr/bin/env python3
"""Entry point into the bot"""

from telegram.ext import ApplicationBuilder
from bot.utils.env import BOT_TOKEN
from bot.handlers.start import start_handler
from bot.handlers.group import chat_member_handler, list_groups, select_group
from bot.handlers.unknown import unknown_handler
from bot.handlers.persistence import persistence
from bot.handlers.topic import topic_handler
from bot.handlers.update_handler import update_handler


application = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence).build()

application.add_handler(start_handler)
application.add_handler(chat_member_handler)
application.add_handler(list_groups)
application.add_handler(select_group)
application.add_handler(unknown_handler)
application.add_handler(topic_handler)
application.add_handler(update_handler)


if __name__ == '__main__':
    print("PHILLIP has started...")
    application.run_polling()
