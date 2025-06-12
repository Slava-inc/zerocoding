from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sqlite3

conn = sqlite3.connect("product.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS product_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image_path TEXT NOT NULL
)
''')

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
browser = webdriver.Chrome(options=options)

browser.get("https://www.wildberries.ru/")
time.sleep(7)

browser.execute_script("window.scrollTo(0, 1000)")
time.sleep(7)
product_links = browser.find_elements(By.CSS_SELECTOR, "a.product-card__link[aria-label]")

i = 1
for product_link in product_links[:10]:
    image_path = f"Screen/product_{i}.png"
    name = product_link.get_attribute("aria-label")
    print(f'{i}: {name}')
    try:
        product_link.screenshot(image_path)
        cursor.execute("INSERT INTO product_list (name, image_path) VALUES (?, ?)", (name, image_path))
        conn.commit()
    except:
        print("Ошибка при сохранении изображения")
    i += 1

for product_link in product_links:
    print(product_link.get_attribute("aria-label"))

browser.quit()
conn.close()