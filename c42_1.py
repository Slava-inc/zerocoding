import telebot
from my_token import TOKEN
import random

bot = telebot.TeleBot(TOKEN)
dishes = [
    "Пицца",
    "Суши",
    "Борщ",
    "Паста",
    "Шашлык",
    "Салат Цезарь",
    "Окрошка",
    "Карбонад",
    "Лагман",
    "Чахохбили"
]
# Обработчик команды /random_dish
@bot.message_handler(commands=['random_dish'])
def send_random_dish(message):
    dish = random.choice(dishes)
    bot.reply_to(message, f"🍲 Сегодня ты будешь есть: **{dish}**!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
     bot.send_message(message.chat.id, "Привет, я бот. Чем я могу вам помочь?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    
    text = message.text.lower()
    
    if "робот" in text:
        bot.send_message(message.chat.id, "Ты упомянул слово 'робот'! Я не робот!")
    else:
        text = message.text.strip()
        words = text.split(" ")
        word_count = len(words)
        char_count_with_spaces = len(text)
        char_count_without_spaces = len(text.replace(" ", ""))
        
        response = (f"Слов: {word_count}\n"
                    f"Символов: {char_count_with_spaces}\n"
                    f"Символов без пробелов: {char_count_without_spaces}\n")
        
        bot.send_message(message.chat.id, response)

bot.delete_webhook(drop_pending_updates=True)
bot.polling()