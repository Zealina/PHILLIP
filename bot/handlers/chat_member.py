#!/usr/bin/env python3
"""This module registers a new group when the bot is added"""

from telegram import Update
from telegram.ext import ChatMemberHandler, ContextTypes
import json


async def added_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prints out any new group addition or removal"""
    print("\n\nThis is from the ChatMemberHandler\n\n")
    print(json.dumps(update.to_dict(), indent=2))


chat_member_handler = ChatMemberHandler(added_to_group)
