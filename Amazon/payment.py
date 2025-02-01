from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json
import time

driver = webdriver.Chrome()
driver.maximize_window()
url = "https://www.amazon.com/HP-Stream-BrightView-Graphics-Bluetooth/dp/B0C4P29ZXH/ref=sr_1_21?dib=eyJ2IjoiMSJ9.cettkJIZ-6qkg07l9TId1WnxhRMFqidXLlksRl4x2Llr72AtzbIO5zUGV535Cs52FzACmsPdn0MurHe5DUyepaOvSZVq8Tp0fz6JBVUIiGWOxsq6-OuQ-iYOurQkKkpoN55mxzuc8bcuM9wfozUSQENiPf8ab4MeyTWYFwe1rP9Qs3fGXIYZvu7zepDGZAaCdu8xfxa5TzL6x2Z3b2XgCbDe62CoTZgveJL4PD2Bne0.i8KqHxzh2vHQGGhymB_UaElpSCdVatZH1zuOS-9Okmg&dib_tag=se&keywords=Laptop&qid=1738412828&sr=8-21"
driver.get(url)

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    
    while True:
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break
        last_height = new_height

time.sleep(10)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.a-button-text'))).click()

time.sleep(25)