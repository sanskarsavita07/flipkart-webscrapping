from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

driver.get("https://www.flipkart.com/")
print("Flipkart page loaded successfully")
time.sleep(5)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME,"Pke_EE"))
)

input_element = driver.find_element(By.CLASS_NAME,"Pke_EE")
input_element.clear()
input_element.send_keys("Smart Watches" + Keys.ENTER)
print("Smart Watches searched through automation")

time.sleep(10)
driver.quit()

