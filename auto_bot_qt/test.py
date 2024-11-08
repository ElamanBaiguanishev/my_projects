import json
import time

from selenium.common import NoSuchElementException
from anwers import answers_phys_culture, answers_history_transport
from tools import Data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

with open('data_ct.json', 'r', encoding='utf-8') as file:
    file_content = file.read()

# Преобразуем содержимое файла в словарь
data_ct = json.loads(file_content)

chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

driver.get(url="https://dot.omgups.ru/login/index.php")

username_field = driver.find_element(by=By.ID, value="username")
password_field = driver.find_element(by=By.ID, value="password")
login_field = driver.find_element(by=By.ID, value="loginbtn")

username_field.send_keys(data_ct["login"])
password_field.send_keys(data_ct["password"])
login_field.click()

driver.get(url="https://dot.omgups.ru/mod/quiz/view.php?id=77816")

# driver.execute_script("window.scrollTo(0, 1000);")
#
# driver.get_screenshot_as_file(f'screenshots\\{user_name}.png')
#
# start_test = driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit'][class='btn btn-secondary']")
#
# start_test.click()
#
# try:
#     find_button = driver.find_element(by=By.ID, value="id_submitbutton")
#     find_button.click()
# except:
#     print("Все норм")
#
# time.sleep(1)
#
# count = 0
#
# time.sleep(10)
#
# div_element = driver.find_element(by=By.CSS_SELECTOR, value="div[class='qn_buttons clearfix multipages']")
# tag_elements = div_element.find_elements(by=By.TAG_NAME, value="a")
#
# print(len(tag_elements))
#
# while count <= len(tag_elements) - 1:
#     try:
#         questions = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='qtext']")
#         button_next = driver.find_element(by=By.CSS_SELECTOR, value="input[type='submit'][name='next']")
#         for question in questions:
#             count = count + 1
#             que = ""
#             try:
#                 que = answers_history_transport[question.text]
#                 if isinstance(que, list):
#                     print("is list")
#                     for i in que:
#                         try:
#                             answer = driver.find_element(by=By.XPATH, value=f"//*[contains(text(), '{i}')]")
#                             answer.click()
#                         except:
#                             print("Не оно")
#                 else:
#                     answer = driver.find_element(by=By.XPATH, value=f"//*[contains(text(), '{que}')]")
#                     answer.click()
#             except Exception as e:
#                 print(e)
#                 que = f"ВОПРОС '{question.text}' ОТВЕТ НЕ НАЙДЕН"
#             print(f"{count}) {que}")
#         button_next.click()
#         time.sleep(1)
#     except NoSuchElementException as e:
#         print(e.msg)
#         time.sleep(100)
#
# driver.execute_script("window.scrollTo(0, 1000);")
#
# driver.save_screenshot(f"screenshots/{user_name}.png")

time.sleep(20000)