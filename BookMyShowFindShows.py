from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException
)
import json
import time

# Initialize WebDriver (ensure you have the correct WebDriver installed and its path set)
driver = webdriver.Chrome()  # You can use webdriver.Firefox(), etc., based on your preference
driver.maximize_window()


    # Navigate to the desired URL
url = "https://in.bookmyshow.com/buytickets/ramayana-the-legend-of-prince-rama-ice-pune/movie-pune-ET00430357-MT/20250128"
driver.get(url)

#//li[@class="list"]


time.sleep(20)