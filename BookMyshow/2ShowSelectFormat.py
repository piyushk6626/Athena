# Book Tickets Button //button[@data-phase="postRelease"] and Contaien Text "Book tickets"
# Multiple Elemnt OF this class="sc-vhz3gb-0 eKTeRz" Which Contain Following Thing
#   Laguage Element = //section[@class="sc-vhz3gb-1 gyUIdc"]
#   Movie Format = //div[@class="sc-vhz3gb-3 ksLpgw"]

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def Show_available_movie_formats(url):
# Initialize WebDriver (make sure to set the correct path to your WebDriver)
    driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc.
    driver.maximize_window()

    try:
        # Navigate to the desired URL
        driver.get(url)

        # Wait until the "Book Tickets" button is visible and clickable
        wait = WebDriverWait(driver, 10)
        book_tickets_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[@data-phase='postRelease'])[1]"))
        )

        # Click the "Book Tickets" button
        book_tickets_button.click() 

        # Wait for the elements to load after clicking
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sc-vhz3gb-0")))

        # Scrape the required data
        movie_elements = driver.find_elements(By.CLASS_NAME, "sc-vhz3gb-0")
        scraped_data = []

        for movie_element in movie_elements:
            try:
                # Extract the language
                language_element = movie_element.find_element(By.XPATH, ".//section[@class='sc-vhz3gb-1 gyUIdc']")
                language = language_element.text

                # Extract all movie formats
                format_elements = movie_element.find_elements(By.XPATH, ".//div[@class='sc-vhz3gb-3 ksLpgw']")
                movie_formats = [format_element.text for format_element in format_elements]

                # Append data to the list
                scraped_data.append({
                    "language": language,
                    "formats": movie_formats
                })
            except Exception as e:
                print(f"Error while scraping data for an element: {e}")

        # Convert the scraped data to JSON
        json_data = json.dumps(scraped_data, indent=4)
        return json_data

    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    url = "https://in.bookmyshow.com/pune/movies/ramayana-the-legend-of-prince-rama/ET00413205"
    json_data = Show_available_movie_formats(url)