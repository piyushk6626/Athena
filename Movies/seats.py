# paytm_scraper/seats.py

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import input_city_and_select_first, select_language, scroll_page, click_button_and_get_url
from .xpath import (
    LAYOUT_CONTAINERS, SEAT_TYPE_PRICE, SEAT_ROWS,
    ROW_NUMBER, SEATING_ELEMENT, BOOK_TICKET_BUTTON,
    QR_CONTAINER
)


class SeatScraper:
    """
    Scrapes seat information from a given URL.
    This class handles the extraction of seat layout and availability information.
    """
    def __init__(self, url):
        """Initialize the scraper with the target URL."""
        self.url = url
        self.driver = webdriver.Chrome()
        self.seat_data = {}

    def parse_seating_layout(self, seating_element):
        """
        Parses the seating layout HTML and returns a list representation:
          0 = blank space
          1 = available seat
         -1 = disabled seat
        """
        seating_list = []
        # Get the HTML content of the seating element
        html_content = seating_element.get_attribute('innerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Process each seat span element
        for span in soup.find_all('span'):
            classes = span.get('class', [])
            # Check for different seat states
            if 'FixedSeatingDesktop_blank__iYFEh' in classes:
                seating_list.append(0)  # Blank space
            elif span.parent and 'FixedSeatingDesktop_tooltipWrap__3nIcb' in span.parent.get('class', []):
                if 'available' in classes:
                    seating_list.append(1)  # Available seat
                elif 'FixedSeatingDesktop_disable__RQsl1' in classes:
                    seating_list.append(-1)  # Disabled seat
        return seating_list

    def get_seat_info(self):
        """
        Scrapes seat information and builds a dictionary with details for each section and row.
        """
        try:
            # Wait for and get all layout containers
            layout_containers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, LAYOUT_CONTAINERS))
            )
            
            # Process each section
            for section_index, container in enumerate(layout_containers):
                # Get seat type and price information
                detail_element = container.find_element(By.XPATH, SEAT_TYPE_PRICE)
                seat_type_price = detail_element.text
                
                # Get all rows in this section
                rows = container.find_elements(By.XPATH, SEAT_ROWS)
                
                # Initialize section data structure
                section_data = {
                    'type_and_price': seat_type_price,
                    'rows': {}
                }
                
                # Process each row
                for row in rows:
                    try:
                        # Get row number and seating layout
                        row_number = row.find_element(By.XPATH, ROW_NUMBER).text
                        seating_element = row.find_element(By.XPATH, SEATING_ELEMENT)
                        seating_layout = self.parse_seating_layout(seating_element)
                        
                        # Store row information
                        section_data['rows'][row_number] = {
                            'seating_layout': seating_layout
                        }
                    except Exception as e:
                        print(f"Error processing row: {e}")
                        continue
                        
                # Store section information
                self.seat_data[f"Section_{section_index + 1}"] = section_data
                
        except Exception as e:
            print(f"An error occurred while extracting seat info: {e}")

    def scrape_seats(self):
        """
        Main method to load the page, scrape seat details, and return the data.
        """
        try:
            # Load the page and get seat information
            self.driver.get(self.url)
            time.sleep(2)
            self.get_seat_info()
            return self.seat_data
        finally:
            self.driver.quit()


def extract_seat_details(url, city, language, theater_name, show_time):
    """
    Navigates to the seat selection page and extracts seat details.
    Returns a tuple of (target_url, seat_data).
    """
    # Set up Chrome options and initialize driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to the page and set up city and language
        input_city_and_select_first(driver, city, url)
        select_language(driver, language)
        scroll_page(driver)
        
        # Get the seat selection URL and scrape seat details
        target_url = click_button_and_get_url(driver, theater_name, show_time)
        scraper = SeatScraper(target_url)
        seat_data = scraper.scrape_seats()
    finally:
        driver.quit()
    return target_url, seat_data


class SeatBooking:
    """
    Provides methods to click on seats, book tickets, and take a screenshot of the payment area.
    Unlike SeatScraper, this class does not quit the browser until after booking.
    """
    def __init__(self, url):
        """Initialize the booking process with the target URL."""
        self.url = url
        self.driver = webdriver.Chrome()
        self.seat_data = {}

    def parse_seating_layout(self, seating_element):
        """
        Parses the seating layout HTML and returns a list representation:
          0 = blank space
          1 = available seat
         -1 = disabled seat
        """
        seating_list = []
        # Get the HTML content of the seating element
        html_content = seating_element.get_attribute('innerHTML')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Process each seat span element
        for span in soup.find_all('span'):
            classes = span.get('class', [])
            # Check for different seat states
            if 'FixedSeatingDesktop_blank__iYFEh' in classes:
                seating_list.append(0)  # Blank space
            elif span.parent and 'FixedSeatingDesktop_tooltipWrap__3nIcb' in span.parent.get('class', []):
                if 'available' in classes:
                    seating_list.append(1)  # Available seat
                elif 'FixedSeatingDesktop_disable__RQsl1' in classes:
                    seating_list.append(-1)  # Disabled seat
        return seating_list

    def get_seat_info(self):
        """
        Scrapes seat information and builds a dictionary with details for each section and row.
        """
        try:
            # Wait for and get all layout containers
            layout_containers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, LAYOUT_CONTAINERS))
            )
            
            # Process each section
            for section_index, container in enumerate(layout_containers):
                # Get seat type and price information
                detail_element = container.find_element(By.XPATH, SEAT_TYPE_PRICE)
                seat_type_price = detail_element.text
                
                # Get all rows in this section
                rows = container.find_elements(By.XPATH, SEAT_ROWS)
                
                # Initialize section data structure
                section_data = {
                    'type_and_price': seat_type_price,
                    'rows': {}
                }
                
                # Process each row
                for row in rows:
                    try:
                        # Get row number and seating layout
                        row_number = row.find_element(By.XPATH, ROW_NUMBER).text
                        seating_element = row.find_element(By.XPATH, SEATING_ELEMENT)
                        seating_layout = self.parse_seating_layout(seating_element)
                        
                        # Store row information
                        section_data['rows'][row_number] = {
                            'seating_layout': seating_layout
                        }
                    except Exception as e:
                        print(f"Error processing row: {e}")
                        continue
                        
                # Store section information
                self.seat_data[f"Section_{section_index + 1}"] = section_data
                
        except Exception as e:
            print(f"An error occurred while extracting seat info: {e}")

    def book_tickets(self, seat_rows, seat_numbers):
        """
        Books tickets for the specified seats.
        Returns a tuple of (seat_data, screenshot_filename).
        """
        # Load the page and get seat information
        self.driver.get(self.url)
        time.sleep(2)
        self.get_seat_info()
        
        # Click on the specified seats
        for row, seat_num in zip(seat_rows, seat_numbers):
            # Construct XPath for the specific seat
            seat_xpath = (
                f"//li[div[@class='FixedSeatingDesktop_seatName__m6_Hm' and text()='{row}']]"
                f"/div[@class='FixedSeatingDesktop_seatL__uU4Pm']"
                f"/div[@class='FixedSeatingDesktop_tooltipWrap__3nIcb'][{seat_num}]/span"
            )
            try:
                # Wait for and click the seat
                seat_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, seat_xpath))
                )
                seat_element.click()
                print(f"Clicked seat at row '{row}', seat index {seat_num}.")
                time.sleep(1)
            except Exception as e:
                print(f"Failed to click seat at row '{row}', seat index {seat_num}: {e}")

        # Click the "Book Ticket" button
        try:
            book_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, BOOK_TICKET_BUTTON))
            )
            book_button.click()
            print("Clicked the 'Book Ticket' button.")
            time.sleep(5)
        except Exception as e:
            print(f"Failed to click the 'Book Ticket' button: {e}")

        # Take a screenshot of the payment QR code
        screenshot_filename = "payment_screenshot.png"
        try:
            # Wait for and locate the QR container
            payment_element = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, QR_CONTAINER))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", payment_element)
            time.sleep(1)
            payment_element.screenshot(screenshot_filename)
            print(f"Payment screenshot saved as '{screenshot_filename}'.")
        except Exception as e:
            print(f"Failed to take payment screenshot: {e}")
            try:
                # Fallback to full page screenshot if QR container not found
                fallback_filename = "full_page_screenshot.png"
                self.driver.save_screenshot(fallback_filename)
                print(f"Full page screenshot saved as '{fallback_filename}'.")
                screenshot_filename = fallback_filename
            except Exception as e2:
                print(f"Also failed to save full page screenshot: {e2}")
                screenshot_filename = None

        # Clean up and return results
        self.driver.quit()
        return self.seat_data, screenshot_filename


def select_given_seat_and_click_book_ticket(url, seat_rows, seat_numbers):
    """
    Opens the URL, clicks the specified seats, clicks the booking button,
    and takes a screenshot of the payment area.
    Returns a tuple: (seat_data, screenshot_filename)
    """
    booking = SeatBooking(url)
    result = booking.book_tickets(seat_rows, seat_numbers)
    return result
