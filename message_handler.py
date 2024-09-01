import sqlite3

from telegram import Update
from telegram.ext import ContextTypes

from create_meme import generate_meme
from utils.database import initialize_database
from utils.templates import TEMPLATES

DB_FILE = 'messages.db'
initialize_database(DB_FILE)


async def handle_text_and_collect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        username = update.effective_user.username

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (chat_id, user_id, username, message) VALUES (?, ?, ?, ?)',
                       (chat_id, user_id, username, text))
        conn.commit()
        conn.close()

        template_choice = context.user_data.get('template', None)
        if not template_choice:
            return
        template_info = TEMPLATES.get(template_choice, 'template1')
        expected_words = len(template_info['text_boxes'])
        texts = update.message.text.split('|')

        if len(texts) == expected_words:
            meme_image = generate_meme(template_info, [text.strip() for text in texts])
            await update.message.reply_photo(photo=meme_image)
            context.user_data['template'] = None
        else:
            await update.message.reply_text(f'Моля, въведете {expected_words} текста, разделени с "|".')
