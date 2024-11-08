# https://dot.omgups.ru/mod/quiz/view.php?id=91742
import json
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from answers import answers
from py_gui import pg_ai

def main_ct():
    options = Options()

    driver_path = "chromedriver.exe"
    s = Service(driver_path)
    driver = webdriver.Chrome(service=s, options=options)

    driver.get(url="https://dot.omgups.ru/login/index.php")

    username_field = driver.find_element(value="username")
    password_field = driver.find_element(value="password")
    login_field = driver.find_element(value="loginbtn")

    with open('data_ct.json', encoding='utf-8') as file:
        file_content = file.read()

    data_ct = json.loads(file_content)

    login = data_ct["login"]
    password = data_ct["password"]
    url = data_ct["url"]

    username_field.send_keys(login)
    password_field.send_keys(password)

    login_field.click()

    driver.get(url)

    start_tests = driver.find_elements(by=By.CSS_SELECTOR,
                                       value="button[type='submit'][class='btn btn-secondary']")
    if len(start_tests) > 1:
        start_test = start_tests[1]
    else:
        start_test = start_tests[0]

    start_test.click()

    time.sleep(2)

    try:
        find_button = driver.find_element(value="id_submitbutton")
        find_button.click()
    except:
        print("Все норм")

    for answer in answers:
        button_next = driver.find_element(by=By.CSS_SELECTOR,
                                          value="input[type='submit'][name='next']")
        for text in answer:
            try:
                answer = driver.find_element(By.XPATH,
                                             f"//*[starts-with(normalize-space(), '{text}')]")
                answer.click()
                print(f"ответил {answer.text}")
            except:
                try:
                    answer = driver.find_element(By.XPATH,
                                                 f"//*[starts-with(normalize-space(), '{text.lower()}')]")
                    answer.click()
                    print(f"ответил {answer.text}")
                except:
                    try:
                        answer = driver.find_element(By.XPATH,
                                                     f"//*[starts-with(normalize-space(), '{text.strip()}')]")
                        answer.click()
                        print(f"ответил {answer.text}")
                    except:
                        try:
                            answer = driver.find_element(by=By.CSS_SELECTOR,
                                                         value="input[type='text'][class='form-control d-inline']")
                            answer.send_keys(text)
                            print(f"ответил {answer.text}")
                        except:
                            traceback.print_exc()
        button_next.click()

    pg_ai()

    time.sleep(6000)
