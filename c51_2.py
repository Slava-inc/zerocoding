import logging
from my_token import TOKEN, OPENWEATHER_API_KEY, CBR_API_URL, WEATHER_LOG_PATH, ADMIN_IDS
import requests #Для выполнения HTTP-запросов к внешним API
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext,MessageHandler,Filters,ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import csv  # Для работы с CSV-файлами (чтение/запись)
from datetime import datetime  # Для работы с датой и временем
import pandas as pd  # Для анализа и обработки данных
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # Для создания графиков и визуализации данных
from io import BytesIO  # Для работы с бинарными потоками в памяти
import os  # Для взаимодействия с файловой системой

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
level=logging.INFO #Уровень логирования
logger = logging.getLogger(__name__) # Создание объекта логгера для текущего модуля

if not os.path.exists(WEATHER_LOG_PATH):
    with open(WEATHER_LOG_PATH, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'user_id', 'username', 'city', 'status'])
else:
    with open(WEATHER_LOG_PATH, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()

        if not first_line.startswith('timestamp') or 'user_id' not in first_line:
            with open(WEATHER_LOG_PATH, 'r+', encoding='utf-8') as f:
                content = f.read()
                f.seek(0, 0)
                f.write('timestamp,user_id,username,city,status\n' + content)

def log_weather_request(user_id: int, username: str, city: str, status: str):
    try:
        with open(WEATHER_LOG_PATH, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file) # Добавляем сюда строку
            writer.writerow([
                datetime.now(),
                user_id,
                username,
                city,
                status])
    except Exception as e:
        logger.error(f"Ошибка записи в лог: {e}")



# Определение состояний для бота (Conversation Handler)
WAIT_CITY, SHOW_INFO, WAIT_CITY_STATS = range(3)  # Состояние диалога: ожидание города и показ информации

def create_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌤 Показать погоду", callback_data='weather')],
        [
            InlineKeyboardButton("💶 Курсы валют", callback_data='currency'),
            InlineKeyboardButton("🖥 Перейти в магазин", url="https://zerocoder.ru")
        ],
        [InlineKeyboardButton("📊 Статистика запросов погоды", callback_data='weather_stats')],

    ]
    return InlineKeyboardMarkup(keyboard) # Создаем разметку клавиатуры

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        "Используйте кнопки ниже или меню: ",
        reply_markup=create_main_menu_keyboard()
    )    

def button_click(update: Update, context: CallbackContext) -> None:
    
    logger.debug(f"Нажата кнопка: {update.callback_query.data}")
    
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
    elif query.data == 'weather_stats':
        query.message.reply_text(
            "Введите название города для получения статистики:",
            reply_markup=ReplyKeyboardRemove()
        )
        return WAIT_CITY_STATS 
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
    user = update.effective_user
    user_id = user.id if user else 0
    username = user.username or user.first_name or "Unknown"
    try:
        response = requests.get(url) # Отправка запроса
        data = response.json() # Парсинг ответа в словарь

        if response.status_code ==200: # Проверка на успешность запроса
            log_weather_request(user_id, username, city, 'success')
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
            log_weather_request(user_id, username, city, 'city_not_found')
            update.message.reply_text(" Город не найден, попробуйте еще раз: ")
            return WAIT_CITY # Повторный запрос города
    except Exception as e:
        log_weather_request(user_id, username, city, 'error')
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

def weather_stats(update: Update, context: CallbackContext):
    if update.effective_user.id not in ADMIN_IDS:
        update.message.reply_text("⚠️ Эта команда доступна только администраторам")
        return
    if not os.path.exists(WEATHER_LOG_PATH) or os.path.getsize(WEATHER_LOG_PATH) == 0:
        update.message.reply_text("📊 Статистика пока недоступна. Запросы еще не делались.")
        return    
    logs = []
    with open(WEATHER_LOG_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  
        for row in reader:
            if not row:
                continue
            if len(row) < 5:
                    row += [''] * (5 - len(row))
            logs.append(row[:5])

        df = pd.DataFrame(logs, columns=['timestamp', 'user_id', 'username', 'city', 'status'])
        if df.empty:
            update.message.reply_text("📊 Статистика пока недоступна. Нет данных для анализа.")
            return
        df['user_id'] = pd.to_numeric(df['user_id'], errors='coerce')
        total_requests = len(df)
        status_counts = df['status'].value_counts()
        success_requests = status_counts.get('success', 0)  # Успешные запросы
        error_requests = status_counts.get('error', 0)  # Ошибки сервера
        city_not_found = status_counts.get('city_not_found', 0)  # Города не найдены
        unique_users = df['user_id'].nunique()  # Уникальные пользователи
        popular_cities = df[df['status'] == 'success']['city'].value_counts().head(5)

        report = (
            f"📊 Статистика запросов погоды:\n"
            f"• Всего запросов: {total_requests}\n"
            f"• Успешных запросов: {success_requests}\n"
            f"• Ошибок 'город не найден': {city_not_found}\n"
            f"• Системных ошибок: {error_requests}\n"
            f"• Уникальных пользователей: {unique_users}\n\n"
            f"🏙️ Топ-5 запрашиваемых городов:\n"        ) 
        if not popular_cities.empty:
            for city, count in popular_cities.items():
                report += f"  - {city}: {count}\n"
        else:
            report += "  Нет данных о городах\n"                     

        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp'])
            if not df.empty:
                df['date'] = df['timestamp'].dt.date
                daily_activity = df.groupby('date').size().reset_index(name='requests')
                daily_activity = daily_activity.sort_values('date', ascending=False).head(7)
                if not daily_activity.empty:
                    report += "\n📅 Активность за последние 7 дней:\n"
                    for _, row in daily_activity.iterrows():
                        report += f"  {row['date']}: {row['requests']} запросов\n"
                else:
                    report += "\n📅 Нет данных о ежедневной активности\n"
            else:
                report += "\n📅 Нет данных о ежедневной активности\n"
        except Exception as e:
            logger.error(f"Ошибка при расчете ежедневной активности: {e}")
            report += "\n📅 Не удалось рассчитать ежедневную активность\n"
        update.message.reply_text(report)
        try:
            if not popular_cities.empty:
                plt.figure(figsize=(10, 6))
                popular_cities.plot(kind='bar', color='skyblue')
                plt.title('Топ запрашиваемых городов')
                plt.ylabel('Количество запросов')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout() 
                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=80)
                buf.seek(0)
                update.message.reply_photo(photo=buf)
                buf.close()
                plt.close()
        except Exception as e:
            logger.error(f"Ошибка генерации статистики: {e}", exc_info=True)
            update.message.reply_text("⚠️ Произошла ошибка при формировании графика")                                   

def main():
    logger.setLevel(logging.DEBUG)  # В начале main()
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_click, pattern='^weather$')],
        states={
            WAIT_CITY: [MessageHandler(Filters.text & ~Filters.command, get_weather)],
            SHOW_INFO: [CallbackQueryHandler(button_click)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )

    conv_handler_weather_stats = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_click, pattern='^weather_stats$')],
        states={
            WAIT_CITY_STATS: [MessageHandler(Filters.text & ~Filters.command, weather_stats)],
            SHOW_INFO: [CallbackQueryHandler(button_click)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
        name="conv_weather_stats"
    )

    # Регистрируем conversation handlers ПЕРВЫМИ!
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(conv_handler_weather_stats)

    # Только нужные callback-обработчики (без общего handler)
    dispatcher.add_handler(CallbackQueryHandler(button_click, pattern='^(currency|back_to_menu|close)$'))

    # Команды
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    logger.info("Бот запущен и готов к работе")

if __name__ == '__main__':    
    main()