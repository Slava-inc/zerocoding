import random

import requests
from bs4 import BeautifulSoup
from my_token import TOKEN

import telebot



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, чем я могу вам помочь?")

@bot.message_handler(commands=['news'])
def send_news(message):
    url = "https://vtomske.ru/"
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        all_titles = soup.find_all('div', class_="lenta_material_title")
        titles = all_titles[-5:]
        for i in range(len(titles)):  # 0, 1, 2, 3, 4
            title_div = titles[i]
            a_tag = title_div.find_parent('a', class_="lenta_material")
            if a_tag and a_tag.has_attr("href"):
                link = a_tag["href"]
                if link.startswith("/"):
                    link = url.rstrip("/") + link
                bot.send_message(message.chat.id, f"{i + 1}. {title_div.text.strip()} \n Ссылка: {link}")
            else:
                bot.send_message(message.chat.id, f"{i + 1}. {title_div.text.strip()} \n Ссылка не найдена")

    else:
        print(f"Ошибка при загрузке страницы {response.status_code}")
        bot.send_message(message.chat.id, "Не удалось получить данные о новостях в Томске!")


bot.polling()