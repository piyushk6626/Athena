#//div[contains(@class, 'MovieSessionsListingDesktop_movieSessions')][.//a[contains(text(), 'PVR Ekmat Chowk, Barshi Road, Latur')]]//div[contains(@class, 'MovieSessionsListingDesktop_timeblock')][.//div[contains(@class, 'MovieSessionsListingDesktop_time') and contains(text(), '09:05 AM')]]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

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

# Example usage
if __name__ == "__main__":
    url ="https://paytm.com/movies/seat-layout/pune/agja3bfpb?encsessionid=1019929-75540-ob22dg-1019929&freeseating=false&fromsessions=true    "  # Replace with actual URL"  # Replace with actual URL
    scraper = SeatScraper(url)
    seat_data = scraper.scrape_seats()
    
    print(seat_data)
    # # Print results
    # for section, section_data in seat_data.items():
    #     print(f"\n{section}:")
    #     print(f"Type and Price: {section_data['type_and_price']}")
    #     print("Rows:")
    #     for row_num, row_data in section_data['rows'].items():
    #         print(f"  Row {row_num}: {row_data['seating_layout']}")
