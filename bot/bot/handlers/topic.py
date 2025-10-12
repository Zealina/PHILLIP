#!/usr/bin/env python3
"""Manage Topics Added to a group"""

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def forum_topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mange all topics in groups that are forums"""
    from json import dumps
    print(dumps(update.to_dict(), indent=4))

fs = filters.StatusUpdate
topic_handler = MessageHandler(
        fs.FORUM_TOPIC_CREATED | fs.FORUM_TOPIC_CLOSED | fs.FORUM_TOPIC_REOPENED | fs.FORUM_TOPIC_EDITED,
        forum_topic_handler)
