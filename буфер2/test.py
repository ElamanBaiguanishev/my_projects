import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from approximate_answer import approximate
from parse_answers import answers

# Устанавливаем опции браузера
options = Options()
options.add_argument(
    "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
)

# Устанавливаем путь к драйверу

driver_path = "C:/Users/Elaman/.wdm/drivers/chromedriver/win64/119.0.6045.160/chromedriver-win32/chromedriver.exe"

s = Service(driver_path)
# Инициализируйте драйвер, указав путь к локальному драйверу
# driver = webdriver.Chrome()

# Инициализируем драйвер
driver = webdriver.Chrome(service=s, options=options)

# Заходим на сайт
driver.get(
    "C:/Users/Elaman/PycharmProjects/release_auto_test_bot/резерв/Тест для защиты курсовой работы (страница 8 из 30).html")
# <input class="input-at" type="text" name="shifr" value="" placeholder="Учебный шифр" autocomplete="off">

answers_ = answers("Электрические машины (ЛТ,ЛЭ)")
# find_ans = driver.find_element(value="question-345413-11")
# print(find_ans.get_attribute('outerHTML'))
# try:
#     answer = driver.find_element(By.XPATH, "//*[text()='120\u00A0град.']")
#     print(answer.text)
# except:
#     traceback.print_exc()
try:
    questions = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='qtext']")
    # button_next = driver.find_element(by=By.CSS_SELECTOR,
    #                                   value="input[type='submit'][name='next']")
    import html

    fixed_pls = driver.find_element(by=By.CSS_SELECTOR, value="div[class='formulation clearfix']")
    html_content = fixed_pls.get_attribute('outerHTML')

    # Преобразование HTML-кода в текст с сохранением &nbsp;
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator=" ", strip=True)
    decoded_text = html.unescape(text_content)

    print(decoded_text)

    # print()
    # print(fixed_pls.get_attribute('outerHTML'))
    # print("&nbsp;" in fixed_pls.get_attribute('outerHTML'))
#     for question in questions:
#         try:
#             que = answers_[question.text]
#         except Exception as e:
#             que = approximate(answers_, question.text)
#         if que is not None:
#             print(question.text)
#             print(que)
#             for text in que:
#                 print(text)
#                 try:
#                     answer = driver.find_element(By.XPATH,
#                                                  f"//*[starts-with(normalize-space(), '{text}')]")
#                     print("kek1")
#                 except Exception as e:
#                     try:
#                         answer = driver.find_element(By.XPATH,
#                                                      f"//*[starts-with(normalize-space(), '{text.lower()}')]")
#                         answer.click()
#                     except Exception as e:
#                         try:
#                             answer = driver.find_element(By.XPATH,
#                                                          f"//*[starts-with(normalize-space(), '{text.strip()}')]")
#                             print("kek2")
#                         except Exception as e:
#                             try:
#                                 answer = driver.find_element(by=By.CSS_SELECTOR,
#                                                              value="input[type='text'][class='form-control d-inline']")
#                                 print("kek3")
#                             except Exception as e:
#                                 traceback.print_exc()
#                                 try:
#                                     print("kek4")
#                                 except Exception as e:
#                                     # Вывод подробной информации об ошибке
#                                     traceback.print_exc()
#                                     print("kek5")
#         else:
#             que = f"ВОПРОС '{question.text}' ОТВЕТ НЕ НАЙДЕН"
#             print(que)
#     # button_next.click()
#     time.sleep(1)
except Exception as e:
    # Вывод подробной информации об ошибке
    print(f"Ошибка при выполнении действий в Selenium: {e}")
    traceback.print_exc()
