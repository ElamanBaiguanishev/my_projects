import time
import traceback

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()

# options.headless = True

options.add_argument(
    "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
)

driver_path = "C:/Users/Elaman/.wdm/drivers/chromedriver/win64/119.0.6045.160/chromedriver-win32/chromedriver.exe"

s = Service(driver_path)

driver = webdriver.Chrome(service=s, options=options)

try:
    driver.get("https://xn--d1ahgpw.xn--p1ai/kabinet.php")

    main_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'][class='input-at'][name='shifr']")
    main_input.send_keys("СП-20-2989")

    ok_button = driver.find_element(value="login")
    print(ok_button.text)
    ok_button.click()

    time.sleep(10)
    menu = driver.find_element(By.CSS_SELECTOR, "ul[class='nav nav-pills nav-fill d-md-flex']")

    semesters = menu.find_elements(by=By.XPATH, value="./*")

    info_div = driver.find_element(by=By.CSS_SELECTOR, value="div[class='tab-content']")

    dolgi_div = ""
    for semester in semesters:
        semester.click()
        div = driver.find_element(value=f"home{semester.text}")
        red = div.find_elements(By.CSS_SELECTOR, "div[style*='background: #ffd5d5;']")
        if red:
            for r in red:
                dolgi_div += r.get_attribute('outerHTML')
                dolgi_div += r.get_attribute('outerHTML')
                dolgi_div += r.get_attribute('outerHTML')

    driver.execute_script('document.body.innerHTML = arguments[0]',
                          info_div.get_attribute('outerHTML') + dolgi_div)

    # Execute the JavaScript code with the dolgi array as an argument
    # driver.execute_script(script, dolgi)
    # sem = driver.find_element(By.CSS_SELECTOR, "a[href='#home4']")
    # sem.click()

    # info_div = driver.find_element(by=By.CSS_SELECTOR, value="div[class='tab-content']")
    #
    # div_element = driver.find_element(value="home4")
    #
    # driver.execute_script('document.body.innerHTML = arguments[0]',
    #                       info_div.get_attribute('outerHTML') + div_element.get_attribute('outerHTML'))

    # sc = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    # driver.set_window_size(sc('Width'),
    #                        sc('Height'))
    # driver.find_element(by=By.TAG_NAME, value='body').screenshot('web_screenshot.png')

    # sem = driver.find_element(By.CSS_SELECTOR, "a[href='#home6']")
    # sem.click()
    # div_elements = driver.find_elements(By.CSS_SELECTOR, "div[style*='background: #ffd5d5;']")
    # for div in div_elements:
    #     div.screenshot("kek.png")
    #     print(div.text)

    print("все успешно")
# except WebDriverException as e:
#     print("kek error", e.msg)
except Exception as e:
    # Вывод подробной информации об ошибке
    print(f"Ошибка при выполнении действий в Selenium: {e}")
    traceback.print_exc()
    time.sleep(60000)

# background: #e0f5d1; border: 1px solid gray; border-radius: 10px; padding: 10px; зеленный цвет
# background: #ffd5d5; border: 1px solid gray; border-radius: 10px; padding: 10px; красный цвет

# background: #ffd5d5; border: 1px solid gray; border-radius: 10px; padding: 10px;

time.sleep(60000)
