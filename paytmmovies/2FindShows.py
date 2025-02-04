from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_page(driver):
    """Scrolls down the page to load dynamic content."""
    current_position = 0
    while True:
        current_position += 5000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break

def extract_movie_shows(driver):
    """Extracts movie show details from the Paytm page."""
    movie_data = []
    try:
        theaters = driver.find_elements(By.XPATH, "//div[@class='MovieSessionsListingDesktop_movieSessions__KYv1d']")
        
        for theater in theaters:
            try:
                name = theater.find_element(By.XPATH, ".//div[@class='MovieSessionsListingDesktop_details__Aq3st']/a").text
                showtimes = []
                
                show_elements = theater.find_elements(By.XPATH, ".//div[contains(@class, 'MovieSessionsListingDesktop_timeblock__MiYNc')]")
                for show in show_elements:
                    try:
                        time_slot_text = show.find_element(By.XPATH, ".//div[contains(@class, 'MovieSessionsListingDesktop_time__r6FAI')]").text
                        time_slot_parts = time_slot_text.split("\n")
                        
                        time_value = time_slot_parts[0]
                        special = time_slot_parts[1] if len(time_slot_parts) > 1 else "N/A"

                        try:
                            movie_format = show.find_element(By.XPATH, ".//div[@class='MovieSessionsListingDesktop_premiumLabel__ed70A']").text
                        except Exception:
                            movie_format = "2D"

                        showtimes.append({
                            "time": time_value,
                            "special": special,
                            "format": movie_format
                        })
                    except Exception:
                        continue
                
                movie_data.append({
                    "theater": name,
                    "shows": showtimes
                })
                
            except Exception:
                continue
    except Exception:
        print("Failed to extract movie details.")
    return movie_data



def input_city_and_select_first(driver, city_name, url):
    """
    Inputs the specified city into the search box and clicks the first result.

    :param driver: Selenium WebDriver instance
    :param city_name: Name of the city to input (string)
    :param url: URL of the webpage containing the city selector (string)
    """
    # Navigate to the specified URL
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)

        # Wait until the search input is present and visible
        search_input = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input.AnimatedSearchBar_animInput__iuqxe")
            )
        )

        # Clear the input box in case it has any pre-filled text
        search_input.clear()

        # Input the city name
        search_input.send_keys(city_name)

        # Optionally, wait for the dropdown to populate
        time.sleep(2)  # Adjust sleep time as necessary for your use case

        dropdown = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="DesktopMovieCitySelector_cityListing__tz4Zf"]')
            )
        )
        # Locate the first result within the dropdown
        first_result = dropdown.find_element(By.XPATH, '(//div[@class="fullHeightScrollDweb DesktopMovieCitySelector_dropdown__PE__h"])[1]')

        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", first_result)

        # Click the first result
        first_result.click()

        print(f"Successfully selected the city: {city_name}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Optional: Close the driver after operation
        # driver.quit()
        pass
def select_language(driver, language):
    try:
        # Wait for the language selection container to appear
        lang_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LanguageSelectionDialog_langSelectionContainer__jZY7u"))
        )
        
        # Find the radio button corresponding to the desired language
        lang_radio = lang_container.find_element(By.XPATH, f"//input[@value='{language}-index']")
        
        # Click the radio button if it exists and is not already selected
        if not lang_radio.is_selected():
            lang_radio.click()
        
        # Click the 'Proceed' button
        proceed_button = driver.find_element(By.CLASS_NAME, "LanguageSelectionDialog_applyBtn__2frJM")
        proceed_button.click()
        
        print(f"Language '{language}' selected successfully.")
    except Exception as e:
        print(f"Error selecting language: {e}")


def Extract_movie_shows(url,city,laguage):
    """
    Extracts movie show details from the Paytm page after selecting the specified city and language.

    :param url: URL of the webpage containing the city selector (string)
    :param city: Name of the city to select (string)
    :param language: Language code to select (string)
    :return: List of dictionaries containing movie show details (list of dict)
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Optional: start maximized
    driver = webdriver.Chrome(options=options)
    # Call the function
    input_city_and_select_first(driver=driver, city_name=city, url=url)        
    select_language(driver=driver, language=laguage)
    scroll_page(driver=driver)
    data=extract_movie_shows(driver=driver)
    return data


if __name__ == "__main__":
    # Path to your ChromeDriver

    # Initialize the Chrome WebDriver
    


    # URL of the webpage with the city selector
    target_url = 'https://paytm.com/movies/deva-movie-detail-167607?frmtid=dimkfeib5'  # Replace with the actual URL

    # Name of the city you want to select
    city_to_select = 'Pune'

    # Call the function
    Data=Extract_movie_shows(target_url,city_to_select,"English")
    print(Data)
    # Optional: Wait to observe the result

