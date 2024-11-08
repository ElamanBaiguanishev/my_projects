import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from approximate_answer import approximate


def start(fio, answers_, login, password, url, semestr, lesson, group, test_name):
    chrome_options = webdriver.ChromeOptions()
    print(answers_)
    chromedriver_path = "resources/chromedriver.exe"

    service = webdriver.chrome.service.Service(chromedriver_path)

    screenshots_path = f"{semestr}/{group}/{lesson}/{test_name}/{fio}/"

    directories = screenshots_path.split('/')

    # Start from the root directory and sequentially check each subdirectory
    current_path = ''
    for directory in directories:
        current_path = os.path.join(current_path, directory)
        if not os.path.exists(current_path):
            os.makedirs(current_path)
            print(f"Folder {current_path} created")
        else:
            print(f"Folder {current_path} already exists")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(url="https://dot.omgups.ru/login/index.php")

        username_field = driver.find_element(by=By.ID, value="username")
        password_field = driver.find_element(by=By.ID, value="password")
        login_field = driver.find_element(by=By.ID, value="loginbtn")

        username_field.send_keys(login)
        password_field.send_keys(password)

        login_field.click()

        driver.get(url=url)

        driver.execute_script("window.scrollTo(0, 1000);")

        driver.save_screenshot(f"{screenshots_path}.start.png")

        start_test = driver.find_element(by=By.CSS_SELECTOR, value="button[type='submit'][class='btn btn-secondary']")

        start_test.click()

        try:
            find_button = driver.find_element(by=By.ID, value="id_submitbutton")
            find_button.click()
        except:
            print("Все норм")

        time.sleep(1)

        count = 0

        time.sleep(5)

        div_element = driver.find_element(by=By.CSS_SELECTOR, value="div[class='qn_buttons clearfix multipages']")
        tag_elements = div_element.find_elements(by=By.TAG_NAME, value="a")

        print(len(tag_elements))

        last_time = driver.find_element(by=By.ID, value="quiz-time-left")

        time_format = "%H:%M:%S"

        time_obj = datetime.strptime(last_time.text, time_format)
        time_in_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

        time_sleep = time_in_seconds / 2

        print("Жду", time_sleep / 60, "минут")

        len_tag_elements = len(tag_elements)

        time_sleep = time_sleep / len_tag_elements

        while count <= len_tag_elements - 1:
            try:
                questions = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='qtext']")
                button_next = driver.find_element(by=By.CSS_SELECTOR, value="input[type='submit'][name='next']")
                print("Жду", time_sleep, "секунд")
                time.sleep(time_sleep)
                for question in questions:
                    print(question.text)
                    count = count + 1
                    try:
                        que = answers_[question.text]
                    except:
                        que = approximate(answers_, question.text)
                    if que is not None:
                        for text in que:
                            try:
                                answer = driver.find_element(By.XPATH, f"//*[starts-with(normalize-space(), '{text}')]")
                                print(answer.tag_name)
                                answer.click()
                                print(f"{count}) {que}")
                            except:
                                try:
                                    answer = driver.find_element(by=By.CSS_SELECTOR,
                                                                 value="input[type='text'][class='form-control d-inline']")
                                    answer.send_keys(que)
                                    print("Нашел на странице инпут для передачи ответа и ввел ответ")
                                    print(f"{count}) {que}")
                                except:
                                    print("Не нашел ответ на странице")
                                    print(f"{count}) {que}")
                    else:
                        que = f"ВОПРОС '{question.text}' ОТВЕТ НЕ НАЙДЕН"
                        print(f"{count}) {que}")
                button_next.click()
                time.sleep(1)
            except NoSuchElementException as e:
                print(e.msg)
                time.sleep(100)

        try:
            end_test = driver.find_element(By.XPATH, "//button[text()='Отправить всё и завершить тест']")
            end_test.click()
        except:
            print("Не нашел конец теста")

        keker(driver)

        driver.get(url=url)

        driver.execute_script("window.scrollTo(0, 1000);")

        driver.save_screenshot(f"{screenshots_path}.final.png")

        time.sleep(60)

    except Exception as e:
        driver.save_screenshot(f"{screenshots_path}.failed.png")
        print(f"ОШИБКА, {e}")


def keker(driver: WebDriver):
    try:
        confirmation_dialog = driver.find_element(by=By.CSS_SELECTOR, value="div[class='confirmation-dialogue']")

        print(confirmation_dialog.text)

        # Найдите дочерний элемент с текстом "Отправить всё и завершить тест"
        submit_button = confirmation_dialog.find_element(By.XPATH,
                                                         ".//input[@value='Отправить всё и завершить тест']")

        # Выполните клик по найденному элементу

        print(submit_button.text)

        submit_button.click()
    except Exception as e:
        print("БРЕД")
        time.sleep(2)
        print(e)
        keker(driver)
