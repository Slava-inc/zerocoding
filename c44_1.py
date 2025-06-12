import requests
from bs4 import BeautifulSoup
import sqlite3

'''db '''
conn = sqlite3.connect('news.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS news(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        link TEXT               
               )
 			''')
conn.commit()


''' Parsing '''
# lenta_material_title
url = "https://vtomske.ru/"
response = requests.get(url)
response.encoding = 'utf-8'

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    all_titles = soup.find_all('div', class_="lenta_material_title")
    titles = all_titles[-5:]
    for i in range(len(titles)): #0, 1, 2, 3, 4
        # print(f"{i + 1}. {titles[i].text.strip()}") # Итоговая строка для вывода новостей
        title_div = titles[i]
        a_tag = title_div.find_parent('a', class_="lenta_material")
        if a_tag and a_tag.has_attr("href"):
            link = a_tag["href"]
            if link.startswith("/"):
                link = url.rstrip("/") + link # rstrip delete end slash url
                cursor.execute("INSERT INTO news (title, link) VALUES (?, ?)", (title_div.text.strip(), link))
                conn.commit()                
                print(f"{i + 1}. {title_div.text.strip()} \n Ссылка: {link}")
        else:
            print(f"{i + 1}. {title_div.text.strip()} \n Ссылка не найдена")    
    # print(titles)
else:
    print(f"Ошибка при загрузке страницы {response.status_code}")
conn.close()