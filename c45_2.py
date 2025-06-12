from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/wiki/Selenium")

search_box = browser.find_element(By.ID, "searchInput")
search_box.send_keys("Python")
search_box.send_keys(Keys.RETURN)
time.sleep(5)
a = browser.find_element(By.LINK_TEXT, "Сетчатый питон")
a.click()
time.sleep(5)


browser.quit()