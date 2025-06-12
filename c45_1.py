from selenium import webdriver
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/wiki/Selenium")
browser.save_screenshot("selenium.png")
time.sleep(5)
browser.refresh()

browser.get("https://ru.wikipedia.org/wiki/%D0%92%D0%B5%D0%B1-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5")
browser.save_screenshot("web.png")
time.sleep(5)
browser.quit()
