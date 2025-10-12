#!/usr/bin/env python3
"""Handle Non-message updates that are not handled by other
handlers"""

from telegram import Update
from telegram.ext import TypeHandler, ContextTypes


async def atypical_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prints out update to standard output"""
    from json import dumps
    print(f"\n>>> Atypical Update Type: {update.update_id}")
    print(dumps(update.to_dict()))


update_handler = TypeHandler(Update, atypical_updates)
