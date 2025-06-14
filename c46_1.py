from my_token import TOKEN
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def create_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌤 Посмотреть погоду", callback_data='weather'),
         InlineKeyboardButton("🖥 Открыть сайт ZeroCoder", url="https://zerocoder.ru")
         ],
          [InlineKeyboardButton("💰 Поддержать", url="https://donate.com")],
          [InlineKeyboardButton("❌ Закрыть", callback_data='close')]
    ]
    return InlineKeyboardMarkup(keyboard) # Создаем разметку клавиатуры

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f"Привет, {user.first_name}! Я твой бот-помощник.Что ты хочешь сделать?",
        # reply_markup=create_main_menu_keyboard()
        reply_markup = create_reply_keyboard()
    )
    update.message.reply_text(
        "Используйте кнопки ниже или меню: ",
        reply_markup=create_main_menu_keyboard()
    )
    

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query # Получаем информацию о нажатии
    query.answer()  # Подтверждаем получение callback (убирает "часики" у кнопки)

    if query.data == "weather":
        back_button = [[InlineKeyboardButton("⬅️ Назад в меню", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(back_button)
        query.edit_message_text(
            text="Функция в разработке, попробуйте позже.", reply_markup=reply_markup
        )
    elif query.data == 'back_to_menu':
        query.edit_message_text(
            text="Выберите действие:",
            reply_markup=create_main_menu_keyboard())
    elif query.data == 'close':
        query.delete_message()

def create_reply_keyboard(): # клавиатура основного меню
    return ReplyKeyboardMarkup(        
         [
            ["🌦 Узнать погоду", "Каталог"],
            ['📞 Контакты', "Мой профиль"],
            [KeyboardButton("Отправить контакт", request_contact=True)],
            [KeyboardButton("Отправить геолокацию", request_location=True)],
         ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    
def create_profile_keyboard():
    return ReplyKeyboardMarkup(
        [["✏️ Изменить имя", "Дата рождения", ["Главное меню"]]],
        resize_keyboard=True,
        one_time_keyboard=True,
            )
    
    
def main():  # Основная функция для настройки и запуска бота
    updater = Updater(TOKEN) # Создаем объект для работы с API Telegram
    dispatcher = updater.dispatcher # Получаем диспетчер для регистрации обработчиков
    dispatcher.add_handler(CommandHandler("start", start)) # через /start
    dispatcher.add_handler(CallbackQueryHandler(button_click)) # через кнопку
    updater.start_polling() # Начинаем опрос сервера Telegram
    updater.idle() # Бот работает до принудительной остановки

if __name__ == '__main__':    
    main()