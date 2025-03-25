# paytm_scraper/utils.py
#
# Utility functions for the Paytm movie booking scraper.
# Contains helper functions for common operations like scrolling, city selection, etc.

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .xpath import (
    CITY_SEARCH_INPUT, CITY_DROPDOWN, FIRST_CITY_RESULT,
    LANG_CONTAINER, LANG_RADIO, PROCEED_BUTTON
)

def scroll_page(driver, step=4000, pause=2):
    """
    Scroll the page in increments to load dynamic content.
    
    Args:
        driver: Selenium WebDriver instance
        step: Number of pixels to scroll each time (default: 4000)
        pause: Time to wait between scrolls in seconds (default: 2)
    """
    current_position = 0
    while True:
        # Scroll down by the specified step
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(pause)
        
        # Check if we've reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break

def input_city_and_select_first(driver, city_name, url):
    """
    Inputs the specified city into the search box and clicks the first result.
    
    Args:
        driver: Selenium WebDriver instance
        city_name: Name of the city to search for
        url: URL of the page to navigate to
    """
    # Navigate to the specified URL
    driver.get(url)
    try:
        # Wait for and find the search input
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, CITY_SEARCH_INPUT))
        )
        
        # Clear and input the city name
        search_input.clear()
        search_input.send_keys(city_name)
        time.sleep(2)
        
        # Wait for and find the city dropdown
        dropdown = wait.until(
            EC.presence_of_element_located((By.XPATH, CITY_DROPDOWN))
        )
        
        # Find and click the first city result
        first_result = dropdown.find_element(By.XPATH, FIRST_CITY_RESULT)
        driver.execute_script("arguments[0].scrollIntoView(true);", first_result)
        first_result.click()
        print(f"Successfully selected the city: {city_name}")
    except Exception as e:
        print(f"An error occurred while selecting city '{city_name}': {e}")

def select_language(driver, language):
    """
    Selects the given language on the page.
    
    Args:
        driver: Selenium WebDriver instance
        language: Language to select (e.g., 'English', 'Hindi')
    """
    try:
        # Wait for and find the language selection container
        lang_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, LANG_CONTAINER))
        )
        
        # Find and select the language radio button
        lang_radio = lang_container.find_element(
            By.XPATH, LANG_RADIO.format(language=language)
        )
        if not lang_radio.is_selected():
            lang_radio.click()
            
        # Click the proceed button
        proceed_button = driver.find_element(By.CLASS_NAME, PROCEED_BUTTON)
        proceed_button.click()
        print(f"Language '{language}' selected successfully.")
    except Exception as e:
        print(f"Error selecting language: {e}")

def click_button_and_get_url(driver, theater_name, show_time):
    """
    Clicks the showtime button for a given theater and show time,
    after scrolling the element into view, then returns the new URL.
    
    Args:
        driver: Selenium WebDriver instance
        theater_name: Name of the theater to select
        show_time: Show time to select
        
    Returns:
        str: The new URL after clicking the show time button
    """
    try:
        # Construct XPath to find the specific show time button
        xpath = (
            f"//div[contains(@class, 'MovieSessionsListingDesktop_movieSessions')][.//a[contains(text(), '{theater_name}')]]"
            f"//div[contains(@class, 'MovieSessionsListingDesktop_timeblock')][.//div[contains(@class, 'MovieSessionsListingDesktop_time') and contains(text(), '{show_time}')]]"
        )
        
        # Find and click the button
        button = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)
        time.sleep(1)  # Allow a moment for the scroll animation to complete
        button.click()
        time.sleep(3)  # Wait for the page to load after clicking
        
        return driver.current_url
    except Exception as e:
        print("Error clicking showtime button:", e)
        return None
