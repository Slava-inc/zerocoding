from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/wiki/Selenium")
time.sleep(5)
paragraphs = browser.find_elements(By.TAG_NAME, "p")
for paragraph in paragraphs:
    print(paragraph.text)
    input()  # пауза после каждого вывода, чтобы не выводился весь текст сразу
    
browser.quit()