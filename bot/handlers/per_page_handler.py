"""
This module handles the per_page command for PHILLIP
It will be imported and added as a handler by main.py
"""

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
from bot.utils.verify import restricted


per_page = 2

@restricted
async def per_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to the per_page command"""
    update_text = update.message.text
    update_text = update_text.split()
    new_value = update_text[-1]
    if new_value.isdigit():
        new_value = int(new_value)
        text = f"Questions Per Page set to: {new_value}"
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        text = "Invalid Number for of questions per page; Set to default of {per_page}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.MARKDOWN)
    global per_page
    per_page = new_value

per_page_handler = CommandHandler('per_page', per_page)
