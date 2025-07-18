"""
This module handles all environment variable loadinf for the PHILLIP bot
It uses `python-dotenv` to load from a `.env` file.

Usage:
    from bot.utils.env import ...
"""

import os
from dotenv import load_dotenv


#Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing from env!")

try:
    OWNER_ID = int(OWNER_ID)
except (TypeError, ValueError):
    raise ValueError("OWNER_ID must be a valid number")
