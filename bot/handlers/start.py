"""
This module handles the start command for PHILLIP
It will be imported and added as a handler by main.py
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
from bot.utils.verify import restricted


@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to the start command"""
    text = (
        f"*Boss {update.effective_user.username}, PHILLIP reporting for duty.*\n\n"
        "_Standing by for your orders...Captain_ 🫡"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.MARKDOWN)

start_handler = CommandHandler('start', start)
