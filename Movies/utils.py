# paytm_scraper/utils.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_page(driver, step=4000, pause=2):
    """Scroll the page in increments to load dynamic content."""
    current_position = 0
    while True:
        current_position += step
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break

def input_city_and_select_first(driver, city_name, url):
    """
    Inputs the specified city into the search box and clicks the first result.
    """
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input.AnimatedSearchBar_animInput__iuqxe")
            )
        )
        search_input.clear()
        search_input.send_keys(city_name)
        time.sleep(2)
        dropdown = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="DesktopMovieCitySelector_cityListing__tz4Zf"]')
            )
        )
        # Locate the first result from the dropdown
        first_result = dropdown.find_element(
            By.XPATH, '(//div[@class="fullHeightScrollDweb DesktopMovieCitySelector_dropdown__PE__h"])[1]'
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", first_result)
        first_result.click()
        print(f"Successfully selected the city: {city_name}")
    except Exception as e:
        print(f"An error occurred while selecting city '{city_name}': {e}")

def select_language(driver, language):
    """
    Selects the given language on the page.
    """
    try:
        lang_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "LanguageSelectionDialog_langSelectionContainer__jZY7u")
            )
        )
        lang_radio = lang_container.find_element(
            By.XPATH, f"//input[@value='{language}-index']"
        )
        if not lang_radio.is_selected():
            lang_radio.click()
        proceed_button = driver.find_element(
            By.CLASS_NAME, "LanguageSelectionDialog_applyBtn__2frJM"
        )
        proceed_button.click()
        print(f"Language '{language}' selected successfully.")
    except Exception as e:
        print(f"Error selecting language: {e}")

def click_button_and_get_url(driver, theater_name, show_time):
    """
    Clicks the showtime button for a given theater and show time,
    after scrolling the element into view, then returns the new URL.
    """
    try:
        xpath = (
            f"//div[contains(@class, 'MovieSessionsListingDesktop_movieSessions')][.//a[contains(text(), '{theater_name}')]]"
            f"//div[contains(@class, 'MovieSessionsListingDesktop_timeblock')][.//div[contains(@class, 'MovieSessionsListingDesktop_time') and contains(text(), '{show_time}')]]"
        )
        button = driver.find_element(By.XPATH, xpath)
        # Scroll the element into view before clicking.
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)
        time.sleep(1)  # Allow a moment for the scroll animation to complete.
        button.click()
        time.sleep(3)  # Wait for the page to load after clicking.
        return driver.current_url
    except Exception as e:
        print("Error clicking showtime button:", e)
        return None
