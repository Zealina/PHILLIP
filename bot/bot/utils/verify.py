"""Verify a users access to the bot"""

from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps
from bot.utils.env import OWNER_ID


def restricted(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user is None:
            return
        if user.id == OWNER_ID:
            return await func(update, context)
        else:
            return await context.bot.reply_text(text="Can't help you sir!", chat_id=update.effective_chat.id)
    return wrapper
