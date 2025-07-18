#!/usr/bin/env python3
"""Handle unknown commands"""

from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from json import dumps


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prints out unknown commands"""
    print(dumps(update.to_dict(), indent=2))

unknown_handler = MessageHandler(filters.ALL, unknown)
