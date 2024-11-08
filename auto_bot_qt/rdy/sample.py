import time

from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()

chromedriver_path = "resources/chromedriver.exe"

service = webdriver.chrome.service.Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(
    "file:///C:/Users/Elaman/Downloads/%D0%A2%D0%B5%D1%81%D1%82%20%D0%9A%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%8F%20%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%B0%20(%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%203%20%D0%B8%D0%B7%2010).html")

text = "машинная графика;"

answer = driver.find_element(By.XPATH, f"//*[starts-with(normalize-space(), '{text}')]")

print(answer.text)

time.sleep(100)

driver.quit()
