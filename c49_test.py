from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
import os
import logging
from dotenv import load_dotenv  # Для загрузки переменных окружения из .env файла


# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    logger.info("Получена команда /start")
    keyboard = [
        [KeyboardButton("/yandex"), KeyboardButton("/sber")],
        [KeyboardButton("/clear")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Привет! Бот запущен.", reply_markup=reply_markup)

def main():

    load_dotenv(dotenv_path='env_vars')
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не найден!")
        return

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    print("Бот запущен. Используйте /start в Telegram.")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()