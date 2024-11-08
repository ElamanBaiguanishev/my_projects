import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import pandas as pd


def answers(name: str) -> dict[str, list[str]]:
    path = f"C:/Users/Elaman/PycharmProjects/clean_py_qt/answers/{name}.xlsx"
    answers_ = {}
    df = pd.read_excel(path, header=None, skiprows=1)

    for _, row in df.iterrows():
        key = row[0].replace("\xa0", " ")  # Удаление неразрывных пробелов
        buff_array = []
        count = 1
        while True:
            try:
                if pd.isna(row[count]):
                    break
                else:
                    buff_array.append(row[count])
                count += 1
            except KeyError:
                break

        answers_[key] = buff_array

    return answers_


# Инициализация браузера
chrome_options = webdriver.ChromeOptions()

chromedriver_path = "C:/Users/Elaman/PycharmProjects/clean_py_qt/resources/chromedriver.exe"

service = webdriver.chrome.service.Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

checked_widgets = ["", "", "", "", "", "", ""]

# for id_ in checked_widgets:
answers_ = answers("Культурология")

try:
    driver.get(url="https://onlinetestpad.com/ar3zw5xmpvdqu")

    questions_count = driver.find_element(by=By.CLASS_NAME, value="otp-item-view-itemscount")

    questions_count = int(questions_count.text.split("Количество вопросов в тесте: ")[1])

    count = 0

    button_next = driver.find_element(by=By.ID, value="btnNext")
    button_next.click()

    while count <= questions_count - 1:
        try:
            questions = driver.find_elements(by=By.CSS_SELECTOR, value="span[class='qtext']")
            button_next = driver.find_element(by=By.ID, value="btnNext")
            for question in questions:
                print(question.text)
                count = count + 1
                que = answers_[question.text]
                if que is not None:
                    for text in que:
                        try:
                            answer = driver.find_element(By.XPATH,
                                                         f"//*[starts-with(normalize-space(), '{text}')]")
                            print(answer.tag_name)
                            answer.click()
                            print(f"{count}) {que}")
                        except:
                            try:
                                answer = driver.find_element(By.XPATH,
                                                             f"//*[starts-with(normalize-space(), '{text.lower()}')]")
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
                                    try:
                                        print(f"{count}) {que}")
                                    except:
                                        print(f"везде ошибка {count}) {que}")
                else:
                    print(f"{count}) {que}")
            button_next.click()
            time.sleep(30)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print(type(traceback.print_exc()))
            traceback.print_exc()

except Exception as e:

    print(f"Произошла ошибка: {e}")

    traceback.print_exc()
