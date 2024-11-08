import sys
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

chrome_options = webdriver.ChromeOptions()

chromedriver_path = "C:/Users/Elaman/PycharmProjects/clean_py_qt/resources/chromedriver.exe"

service = webdriver.chrome.service.Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("C:\\Users\\Elaman\\Desktop\\Тест (страница 1 из 20).html")

try:
    answers_page = driver.find_elements(By.CSS_SELECTOR, ".flex-fill.ml-1")

    print(answers_page[0].parent)
    print(answers_page[0].text)
    print(answers_page[0].text)

    buff = ""

    fixed_pls = driver.find_element(by=By.CSS_SELECTOR,
                                    value="div[class='formulation clearfix']")

    print(fixed_pls.text)


except Exception as e:
    print(f"ОШИБКА, {e}", sys.exc_info())
    time.sleep(60)
