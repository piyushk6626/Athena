from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

class SeatScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.seat_data = {}

    def parse_seating_layout(self, seating_element):
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
        try:
            layout_containers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[@class="FixedSeatingDesktop_layoutCon__vNrYG"]')
                )
            )
            for section_index, container in enumerate(layout_containers):
                detail_element = container.find_element(
                    By.XPATH, 
                    './/div[@class="FixedSeatingDesktop_detaDetail__5yNOt"]/div'
                )
                seat_type_price = detail_element.text
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
                        row_number = row.find_element(
                            By.XPATH,
                            './/div[@class="FixedSeatingDesktop_seatName__m6_Hm"]'
                        ).text
                        seating_element = row.find_element(
                            By.XPATH,
                            './/div[@class="FixedSeatingDesktop_seatL__uU4Pm"]'
                        )
                        seating_layout = self.parse_seating_layout(seating_element)
                        section_data['rows'][row_number] = {'seating_layout': seating_layout}
                    except Exception as e:
                        print(f"Error processing row: {str(e)}")
                        continue
                self.seat_data[f"Section_{section_index + 1}"] = section_data
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    def scrape_seats(self):
        self.driver.get(self.url)
        time.sleep(2)
        self.get_seat_info()
        return self.seat_data


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


# Example usage:
if __name__ == "__main__":
    try:
        seat_data, screenshot = Select_Given_Seat_and_Click_Book_Ticket(
            url="https://example.com",  # This is overwritten in the function
            seatrow=["B", "C"],
            seatnumber=[3, 4]
        )
        print("Seat data scraped:")
        print(seat_data)
        if screenshot:
            print(f"Screenshot saved as: {screenshot}")
        else:
            print("No screenshot was captured.")
    except Exception as e:
        print(f"An error occurred during the booking process: {str(e)}")
