from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Navigate to the URL
url = "https://in.bookmyshow.com/buytickets/mufasa-the-lion-king-pune/movie-pune-ET00396541-MT/20250131"
driver.get(url)

def scroll_page(driver):
    """Scroll the page to load all dynamic JavaScript content"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    while True:
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break

# Scroll to ensure all data is loaded

time.sleep(5)  # Allow content to load

#//li[@class="list" and @data-name="MovieMax Edition (Luxe): Amanora Town Center, Pune"]//a[@class="showtime-pill" and @data-display-showtime="10:45 AM"]
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@class="list" and @data-name="MovieMax Edition (Luxe): Amanora Town Center, Pune"]//a[@class="showtime-pill" and @data-display-showtime="10:45 AM"]'))).click()
   
time.sleep(10) 