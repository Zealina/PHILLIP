#!/usr/bin/env python3
"""Entry point into the bot"""

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot.utils.env import BOT_TOKEN
from bot.handlers.start import start_handler
from bot.handlers.group import chat_member_handler, list_groups, select_group
from bot.handlers.unknown import unknown_handler
from bot.handlers.persistence import persistence
from bot.handlers.topic import topic_handler
from bot.handlers.update_handler import update_handler
from telegram.constants import ParseMode



VISION_TEXT = """
*PHILLIP Bot Vision* 🤖

PHILLIP is a Telegram-based personal assistant designed to help a medical student stay organized, learn efficiently, and grow through each clinical posting.  
_Built by a med student, for med students._

---

*🎯 Core Purpose:*  
To gather, organize, and analyze all your learning materials — past questions, clinical cases, audio notes, and more — into one smart assistant that understands your learning style and helps you focus on what matters most.

---

*📂 Main Features:*

1. *Topic Buckets*  
   - Notes  
   - Past questions  
   - Diagrams/images  
   - Audio recordings (lectures, ward rounds)  
   - AI-generated: summaries, flashcards, transcripts, quizzes  

2. *Clinical Rotation Assistant*  
   - Track your current posting (e.g., Pediatrics, Surgery)  
   - Log ward round cases  
   - Get study prompts based on rotation  
   - _Planned:_ Tag cases under topics for quick retrieval  

3. *Audio Analyzer*  
   - Upload or record lectures/ward rounds  
   - Automatic transcription  
   - Highlights key points  
   - Suggests parts to replay  
   - Generates flashcards & summaries  

4. *Question Bank Manager*  
   - Parse past questions from docs  
   - Save & organize by topic  
   - Quiz via Telegram  
   - Track weak spots and improve  

5. *Smart Learning System*  
   - Adjusts difficulty based on your performance  
   - Reminds you about tough or frequently missed topics  
   - Future vision: PHILLIP adapts when you're tired, overwhelmed, or thriving

---

*🧪 Current MVP Focus:*  
- Group and topic registration  
- Uploading and storing questions  
- Topic-based content buckets  
- Basic clinical logging  
- Audio features are in development  

---

*🏁 Final Goal:*  
A personal learning assistant that evolves with your needs throughout med school — knows your strengths, boosts your weak spots, and keeps you grounded during hectic clinical postings.
"""

async def vision_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(VISION_TEXT, parse_mode='Markdown')


vision_handler = CommandHandler('vision', vision_handler)

application = ApplicationBuilder().token(BOT_TOKEN).persistence(persistence).build()

application.add_handler(start_handler)
application.add_handler(chat_member_handler)
application.add_handler(list_groups)
application.add_handler(select_group)
application.add_handler(vision_handler)
application.add_handler(unknown_handler)
application.add_handler(topic_handler)
application.add_handler(update_handler)


if __name__ == '__main__':
    print("PHILLIP has started...")
    application.run_polling()
