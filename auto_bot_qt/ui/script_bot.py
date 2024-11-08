import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from rdy.parsing_excel_log_pass import result, list_fio


def start(login, password):
    try:

        print(login, password)

        chrome_options = Options()

        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url="https://dot.omgups.ru/login/index.php")

        username_field = driver.find_element(by=By.ID, value="username")
        password_field = driver.find_element(by=By.ID, value="password")
        login_field = driver.find_element(by=By.ID, value="loginbtn")

        username_field.send_keys(login)
        password_field.send_keys(password)
        login_field.click()

        time.sleep(10)

        driver.save_screenshot(f"{login, password}.png")

        time.sleep(10)
    except Exception as e:
        print(f"ОШИБКА, {e}")
