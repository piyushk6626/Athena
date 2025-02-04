from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import time
import json

def scroll_page(driver):
    """Scroll the page by 1000px increments to load dynamic JavaScript content"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    
    while True:
        # Scroll down by 1000 pixels
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2)  # Adjust sleep time based on page loading speed
        
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break
        
        last_height = new_height

def scrape_movies(city):
    url = f"https://paytm.com/movies/{city}"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    try:
        # Click 'View More' button if available
        view_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='ViewMore_viewAll__KJ5c1']/span"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", view_more_button)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, -200);")  # Move up slightly before clicking
        time.sleep(1)
        driver.execute_script("arguments[0].click();", view_more_button)

        time.sleep(3)  # Wait for new content to load
    except (NoSuchElementException, TimeoutException):
        print("No 'View More' button found or clickable.")

    # Scroll to the bottom to load all movies
    scroll_page(driver)

    # Scrape movie details
    movies = []
    movie_elements = driver.find_elements(By.XPATH, "//div[@class='DesktopRunningMovie_movieCard__p5n6P']")
    
    for movie in movie_elements:
        try:
            poster = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_imgCon__XM_UA']/img").get_attribute("src")
            link = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_runningMovie__N17Hp']/a").get_attribute("href")
            title = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_movTitle__Q1pOY']").text
            age_rating = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_point__YtD_w']/span").text
            language = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_point__YtD_w']/span[@class='textClamp']").text
            
            movies.append({
                "title": title,
                "poster": poster,
                "link": link,
                "age_rating": age_rating,
                "language": language
            })
        except NoSuchElementException:
            continue
    
    driver.quit()
    return json.dumps(movies, indent=4)
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
    

class SeatScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.seat_data = {}

    def parse_seating_layout(self, seating_element):
        """
        Parse the seating layout HTML and return a list representation
        0 = blank space
        1 = available seat
        -1 = disabled seat
        """
        seating_list = []
        html_content = seating_element.get_attribute('innerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for span in soup.find_all('span'):
            if 'FixedSeatingDesktop_blank__iYFEh' in span.get('class', []):
                seating_list.append(0)
            elif span.parent and 'FixedSeatingDesktop_tooltipWrap__3nIcb' in span.parent.get('class', []):
                if 'available' in span.get('class', []):
                    seating_list.append(1)
                elif 'FixedSeatingDesktop_disable__RQsl1' in span.get('class', []):
                    seating_list.append(-1)
        
        return seating_list

    def get_seat_info(self):
        """
        Scrape seat information and create a dictionary with seat details for multiple rows
        """
        try:
            # Wait for the seating layout containers (sections) to be present
            layout_containers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[@class="FixedSeatingDesktop_layoutCon__vNrYG"]')
                )
            )

            for section_index, container in enumerate(layout_containers):
                # Get seat type and price for the section
                detail_element = container.find_element(
                    By.XPATH, 
                    './/div[@class="FixedSeatingDesktop_detaDetail__5yNOt"]/div'
                )
                seat_type_price = detail_element.text

                # Find all rows in this section
                rows = container.find_elements(
                    By.XPATH,
                    './/div[@class="FixedSeatingDesktop_rightRow__FnHaS"]/ul/li'
                )

                section_data = {
                    'type_and_price': seat_type_price,
                    'rows': {}
                }

                for row in rows:
                    try:
                        # Get row number
                        row_number = row.find_element(
                            By.XPATH,
                            './/div[@class="FixedSeatingDesktop_seatName__m6_Hm"]'
                        ).text

                        # Get seating layout element
                        seating_element = row.find_element(
                            By.XPATH,
                            './/div[@class="FixedSeatingDesktop_seatL__uU4Pm"]'
                        )

                        # Parse the seating layout
                        seating_layout = self.parse_seating_layout(seating_element)

                        # Add row data to section
                        section_data['rows'][row_number] = {
                            'seating_layout': seating_layout
                        }

                    except Exception as e:
                        print(f"Error processing row: {str(e)}")
                        continue

                # Add section data to main dictionary
                self.seat_data[f"Section_{section_index + 1}"] = section_data

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def scrape_seats(self):
        """
        Main method to start scraping process
        """
        try:
            self.driver.get(self.url)
            time.sleep(2)  # Allow page to load completely
            self.get_seat_info()
            return self.seat_data
        finally:
            self.driver.quit()


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

def click_button_and_get_url(driver,theater_name,show_time):
    try:
        # XPath for the button
        xpath = f"//div[contains(@class, 'MovieSessionsListingDesktop_movieSessions')][.//a[contains(text(), {theater_name})]]//div[contains(@class, 'MovieSessionsListingDesktop_timeblock')][.//div[contains(@class, 'MovieSessionsListingDesktop_time') and contains(text(), '{show_time}')]]"
        
        # Find the button
        button = driver.find_element(By.XPATH, xpath)
        
        # Click the button
        button.click()
        
        # Wait for page to load (Adjust time as needed)
        time.sleep(3)
        
        # Get the current URL after clicking
        return driver.current_url
    except Exception as e:
        print("Error:", e)
        return None


def Extract_seat_Details(url,city,laguage,theater_name,show_time):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Optional: start maximized
        driver = webdriver.Chrome(options=options)
        # Call the function
        input_city_and_select_first(driver=driver, city_name=city, url=url)        
        select_language(driver=driver, language=laguage)
        scroll_page(driver=driver)
        url=click_button_and_get_url(driver=driver,theater_name=theater_name,show_time=show_time)
        scraper = SeatScraper(url)
        seat_data = scraper.scrape_seats()
        return seat_data            
    finally:
        # Ensure the browser is closed after completion
        driver.quit()    

def Select_Given_Seat_and_Click_Book_Ticket(url, seatrow: list, seatnumber: list):
    """
    Opens the URL, scrapes seat data, clicks the given seats, clicks the booking button,
    and then takes a screenshot of the payment (QR) container.
    
    Returns a tuple: (seat_data, screenshot_filename)
    """
    # Overwrite URL if necessary
    scraper = SeatScraper(url)
    seat_data = scraper.scrape_seats()
    
    # Click on specified seats
    for row, seat_num in zip(seatrow, seatnumber):
        seat_xpath = (
            f"//li[div[@class='FixedSeatingDesktop_seatName__m6_Hm' and text()='{row}']]"
            f"/div[@class='FixedSeatingDesktop_seatL__uU4Pm']"
            f"/div[@class='FixedSeatingDesktop_tooltipWrap__3nIcb'][{seat_num}]/span"
        )
        try:
            seat_element = WebDriverWait(scraper.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, seat_xpath))
            )
            seat_element.click()
            print(f"Clicked seat at row '{row}', seat index {seat_num}.")
            time.sleep(1)
        except Exception as e:
            print(f"Failed to click seat at row '{row}', seat index {seat_num}: {str(e)}")
    
    # Click the "Book Ticket" button
    book_button_xpath = (
        "//button[@class='Button_btn___t8GZ Button_is-primary__Z7vVN Button_is-large__GjSIq "
        "SeatLayoutFooterDesktop_bookTicket__B0fUV']"
    )
    try:
        book_button = WebDriverWait(scraper.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, book_button_xpath))
        )
        book_button.click()
        print("Clicked the 'Book Ticket' button.")
        time.sleep(5)  # Wait for the payment screen to load
    except Exception as e:
        print(f"Failed to click the 'Book Ticket' button: {str(e)}")
    
    # Additional sleep to ensure the payment screen is ready
    time.sleep(3)
    
    # Attempt to take a screenshot of the payment screen
    screenshot_filename = "payment_screenshot.png"
    try:
        # Use a flexible XPath with contains() to find the payment container
        screenshot_xpath = "//div[contains(@class, 'qrContainer')]"
        payment_element = WebDriverWait(scraper.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, screenshot_xpath))
        )
        # Scroll element into view
        scraper.driver.execute_script("arguments[0].scrollIntoView(true);", payment_element)
        time.sleep(1)
        payment_element.screenshot(screenshot_filename)
        print(f"Payment screenshot saved as '{screenshot_filename}'.")
    except Exception as e:
        print(f"Failed to take payment screenshot: {str(e)}")
        # Fallback: Save a full-page screenshot
        try:
            fallback_filename = "full_page_screenshot.png"
            scraper.driver.save_screenshot(fallback_filename)
            print(f"Full page screenshot saved as '{fallback_filename}'.")
            screenshot_filename = fallback_filename
        except Exception as e2:
            print(f"Also failed to save full page screenshot: {str(e2)}")
            screenshot_filename = None

    # Ensure that the function returns a tuple even if errors occur
    return seat_data, screenshot_filename

