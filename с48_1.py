import logging
from my_token import TOKEN, OPENWEATHER_API_KEY, CBR_API_URL
import requests #Для выполнения HTTP-запросов к внешним API
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,MessageHandler,Filters,ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
level=logging.INFO #Уровень логирования
logger = logging.getLogger(__name__) # Создание объекта логгера для текущего модуля

# Определение состояний для бота (Conversation Handler)
WAIT_CITY, SHOW_INFO = range(2)  # Состояние диалога: ожидание города и показ информации

def create_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌤 Показать погоду", callback_data='weather')],
        [
            InlineKeyboardButton("💶 Курсы валют", callback_data='currency'),
            InlineKeyboardButton("🖥 Перейти в магазин", url="https://zerocoder.ru")
        ]

    ]
    return InlineKeyboardMarkup(keyboard) # Создаем разметку клавиатуры

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        "Используйте кнопки ниже или меню: ",
        reply_markup=create_main_menu_keyboard()
    )    

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query # Получаем информацию о нажатии
    query.answer()  # Подтверждаем получение callback (убирает "часики" у кнопки)

    if query.data == "weather":
        query.message.reply_text(
               "Введите название города:",
            reply_markup=ReplyKeyboardRemove() # Удаление клавиатуры
        )
        return WAIT_CITY # Переход в состояние ожидания города
    elif query.data == 'currency':
        show_currency_rates(query) # Вызов функции показа курсов валют
        return SHOW_INFO # Переход в состояние показа информации
    elif query.data == 'back_to_menu':
        query.edit_message_text(
            text="Главное меню: ",
            reply_markup=create_main_menu_keyboard()
        )
        return ConversationHandler.END # Завершение диалога
    elif query.data == 'close':
        query.delete_message()

def cancel (update:Update, context:CallbackContext) ->int:
    """Отмена текущего действия"""
    update.message.reply_text("Действие отменено", reply_markup=create_main_menu_keyboard()) # Возврат основной клавиатуры 


def get_weather(update:Update, context:CallbackContext) ->int:
    city = update.message.text # Получение города из сообщения пользователя
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url) # Отправка запроса
        data = response.json() # Парсинг ответа в словарь
        if response.status_code ==200: # Проверка на успешность запроса
            weather_info = (
                f" Погода в {city}:\n"
                f" Температура: {data['main']['temp']} °C\n"
                f" Состояние: {data['weather'][0]['description']} \n"
                f" Влажность: {data['main']['humidity']} %\n"
                f" Ветер: {data['wind']['speed']} м/с"
            )
                # Кнопка возврата
            keyboard = [[InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]]
            update.message.reply_text(weather_info,reply_markup=InlineKeyboardMarkup(keyboard))
            return SHOW_INFO # Переход в состояние показа информации
        else:
            # Если город не найден
            update.message.reply_text(" Город не найден, попробуйте еще раз: ")
            return WAIT_CITY # Повторный запрос города
    except Exception as e:
        logger.error(f"Ошибка при получении информации о погоде: {e}") # Логирование ошибки
        update.message.reply_text("Произошла ошибка. Попробуйте позже")
        return ConversationHandler.END #Завершение диалога

def show_currency_rates(query):
    try:
        response = requests.get(CBR_API_URL) # API запрос к ЦБ
        data = response.json() # Парсинг JSON-ответа
        rates = data['Valute'] # Извлечение данных о валютах
        text = (
            f"Курсы ЦБ РФ:\n"
            f"Доллар USA: {rates['USD']['Value']:.2f} ₽\n"
                        f"Евро: {rates['EUR']['Value']:.2f} ₽\n"
            f"Юань: {rates['CNY']['Value']:.2f} ₽\n"
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]]
        query.edit_message_text(
            text=text, reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.error(f"Ошибка при получении курса валют: {e}") # Логирование ошибки
        query.edit_message_text ("Не удалось получить курсы валют") # Сообщения об ошибке для бота


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_click, pattern='^weather$')],
                states={
            WAIT_CITY:[MessageHandler(Filters.text & ~Filters.command, get_weather)],
# Ожидание города
            SHOW_INFO:[CallbackQueryHandler(button_click)] # Состояние показа информации
        },
        fallbacks=[CommandHandler('cancel',cancel)], # Резеврный обработчик отмены
        allow_reentry=True # Разрешение на повторный диалог
    )
    dispatcher.add_handler(conv_handler) # Диалог погоды
    dispatcher.add_handler(CallbackQueryHandler(button_click, pattern='^(currency|back_to_menu|close)$')) # через кнопку
    dispatcher.add_handler(CommandHandler("start", start)) # через /start
    dispatcher.add_handler(CallbackQueryHandler(button_click)) # через кнопку

    
    updater.start_polling()
    logger.info("Бот запущен и готов к работе")

if __name__ == '__main__':    
    main()