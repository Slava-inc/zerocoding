import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from my_token import TOKEN

BITRIX_WEBHOOK_URL = 'https://b24-bm375m.bitrix24.ru/rest/1/01luvzkgcpg6ufwx/'
url = 'https://b24-bm375m.bitrix24.ru/rest/1/01luvzkgcpg6ufwx/profile.json'

def create_bitrix_lead(name: str, phone: str, comment: str = "") -> dict:
    url = f"{BITRIX_WEBHOOK_URL}crm.lead.add.json"
    data = {
        "fields": {
            "TITLE": f"Заявка от {name}",
            "NAME": name,
            "PHONE": [{"VALUE": phone}],
            "COMMENTS": f"Источник: Telegram Bot\n{comment}"
        }
    }
    response = requests.post(url, json=data)
    return response.json()

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "📝 Отправьте данные в формате:\n"
        "<b>Имя Телефон [Комментарий]</b>\n\n"
        "Пример: <code>Иван +79123456789 Хочу узнать про скидки</code>",
        parse_mode="HTML"
    )

def handle_message(update: Update, context: CallbackContext):
    try:
        text = update.message.text.split(maxsplit=2)
        name, phone = text[0], text[1]
        comment = text[2] if len(text) > 2 else ""
        result = create_bitrix_lead(name, phone, comment)
        if 'result' in result:
            update.message.reply_text(f"✅ Заявка создана!\nID: {result['result']}")
        else:
            error = result.get('error_description', 'Неизвестная ошибка')
            update.message.reply_text(f"❌ Ошибка: {error}")
    except Exception as e:
        update.message.reply_text("⚠️ Ошибка формата. Пример:\n<code>Иван +79123456789</code>", parse_mode="HTML")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

    print("🤖 Бот запущен...")

if __name__ == '__main__':
    main()