import os
import sqlite3

from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

from message_handler import DB_FILE


async def generate_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    num_messages = int(context.args[0])

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT user_id, username, message 
        FROM messages 
        WHERE chat_id = {chat_id} 
        ORDER BY id DESC 
        LIMIT {num_messages}
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("Няма налични съобщения за резюме.")
        return

    collected_messages = [f"{row[1] or 'Непознат'} (ID: {row[0]}): {row[2]}" for row in rows]

    messages_text = "\n".join(collected_messages)

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),

    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user",
             "content": f"Обобщи следната дискусия в кратко резюме:\n\n{messages_text}"}
        ],
        max_tokens=128000,
        temperature=0.5
    )

    summary = response.choices[0].message.content.strip()

    await update.message.reply_text(f"Резюме на последните {num_messages} съобщения:\n\n{summary}")
