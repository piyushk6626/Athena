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

def Find_Show_url_for_given_format(url, language, format_):
    # Initialize WebDriver (ensure you have the correct WebDriver installed and its path set)
    driver = webdriver.Chrome()  # You can use webdriver.Firefox(), etc., based on your preference
    driver.maximize_window()

    try:
        # Navigate to the desired URL
        driver.get(url)

        # Initialize WebDriverWait with a timeout of 20 seconds
        wait = WebDriverWait(driver, 20)

        # ============================
        # Step 1: Click the "Book Tickets" Button
        # ============================
        try:
            # Wait until the "Book Tickets" button is visible and clickable
            book_tickets_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@data-phase='postRelease']")
                )
            )
            # Scroll the button into view
            driver.execute_script("arguments[0].scrollIntoView(true);", book_tickets_button)
            # Click the "Book Tickets" button
            book_tickets_button.click()
            print("Clicked the 'Book Tickets' button.")
        except TimeoutException:
            print("Timed out waiting for the 'Book Tickets' button to become clickable.")
            driver.quit()
            exit(1)
        except Exception as e:
            print(f"An error occurred while clicking the 'Book Tickets' button: {e}")
            driver.quit()
            exit(1)
        
        # ============================
        # Step 2: Select Language and Format
        # ============================
        try:

            # Construct the improved XPath using 'contains' for class attributes
            xpath_expression = f"""
            //li[
                section[contains(@class, 'gyUIdc')]/span[text() = '{language}']
            ]
            /section[contains(@class, 'cNoOUD')]
            /div[contains(@class, 'ksLpgw')][span[text() = '{format_}']]
            """

            # Wait until the desired format element is clickable
            format_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath_expression))
            )

            # Optionally, scroll the element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", format_element)

            # Click the desired format element
            format_element.click()
            print(f"Clicked the '{format_}' format for '{language}' language.")
        except TimeoutException:
            print(f"Timed out waiting for the '{format_}' format element to become clickable.")
            driver.quit()
            exit(1)
        except ElementClickInterceptedException:
            print(f"The '{format_}' format element was not clickable (possibly obscured).")
            driver.quit()
            exit(1)
        except NoSuchElementException:
            print(f"The '{format_}' format element was not found in the DOM.")
            driver.quit()
            exit(1)
        except Exception as e:
            print(f"An error occurred while selecting the format: {e}")
            driver.quit()
            exit(1)
        time.sleep(2)    
        final_url = driver.current_url
        print(f"Final URL after actions: {final_url}")


        
    finally:
        # Close the browser after all operations
        driver.quit()
        print("Browser closed.")
        
if __name__ == "__main__":
    url = "https://in.bookmyshow.com/pune/movies/ramayana-the-legend-of-prince-rama/ET00413205"
    language = "Hindi"
    format_ = "ICE"
    Find_Show_url_for_given_format(url, language, format_)
    
    