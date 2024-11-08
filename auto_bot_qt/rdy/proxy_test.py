import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# 5.254.34.49:3129
# 107.151.193.8:45787
# proxy_address = "71.19.252.28:8443"  # IP:PORT or HOST:PORT

chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument(f'--proxy-server={proxy_address}')

# Path to the ChromeDriver executable
chromedriver_path = "resources/chromedriver.exe"

# Create a Service instance for the ChromeDriver
service = webdriver.chrome.service.Service(chromedriver_path)

# Create Chrome WebDriver instance with options and service
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url="https://dot.omgups.ru/login/index.php")

username_field = driver.find_element(by=By.ID, value="username")
password_field = driver.find_element(by=By.ID, value="password")
login_field = driver.find_element(by=By.ID, value="loginbtn")

username_field.send_keys("pidanovma_70lt_90281")
password_field.send_keys("Max#90281")

login_field.click()

# Load the webpage through the proxy
driver.get("https://dot.omgups.ru/mod/quiz/summary.php?attempt=303758&cmid=70988")

try:
    end_test = driver.find_element(By.XPATH, "//button[text()='Отправить всё и завершить тест']")
    end_test.click()
except:
    print("Не нашел конец теста")

time.sleep(5)

try:
    confirmation_dialog = driver.find_element(by=By.CSS_SELECTOR, value="div[class='confirmation-dialogue']")

    print(confirmation_dialog.text)

    # Найдите дочерний элемент с текстом "Отправить всё и завершить тест"
    submit_button = confirmation_dialog.find_element(By.XPATH,
                                                     ".//input[@value='Отправить всё и завершить тест']")

    # Выполните клик по найденному элементу

    print(submit_button.text)

    submit_button.click()
except:
    print("Не смог найти подтверждение окончания теста")


time.sleep(100)

# Close the browser
driver.quit()
