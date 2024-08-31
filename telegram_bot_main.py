import os

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from create_meme import start, handle_button
from message_handler import handle_text_and_collect
from summarize import generate_summary

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


def main() -> None:
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("meme", start))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_and_collect))
    application.add_handler(CommandHandler("summary", generate_summary))

    application.run_polling()


if __name__ == '__main__':
    main()
