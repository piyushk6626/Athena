from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from urllib.parse import urlparse, parse_qs
import re 

def scrape_airbnb(destination, checkinDate, checkoutDate, adultsNo, childrenNo):
    # Initialize Chrome options
    """
    Scrape Airbnb for hotels based on destination, check-in date, check-out date, number of adults, and number of children.

    Args:
        destination (str): Destination for searching hotels.
        checkinDate (str): Check-in date for booking.
        checkoutDate (str): Check-out date for booking.
        adultsNo (str): Number of adults.
        childrenNo (str): Number of children.

    Returns:
        dict: Dictionary containing a list of hotel data and a type field with value 'airbnb'.
    """
    chrome_options = Options()
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")

    # Automatically manage ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    url = f"https://www.airbnb.co.in/s/{destination}/homes?checkin={checkinDate}&checkout={checkoutDate}&adults={adultsNo}&children={childrenNo}&query={destination}"
    
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    hotels_data = []
    
    def clean_text(text):
        text = re.sub(r'\n+', ' ', text)  # Replace newlines with spaces
        text = re.sub(r'[^\x20-\x7E]', '', text)  # Remove non-ASCII characters
        return text.strip()
    
    def extract_hotels():
        hotels = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
        
        for hotel in hotels[:10]:
            try:
                image_elements = hotel.find_elements(By.XPATH, './/div/picture/img')
                image_url = image_elements[0].get_attribute('src') if image_elements else ""
                hotel_name = clean_text(hotel.find_element(By.XPATH, './/div[contains(@class, "t1jojoys")]').text)
                payment_url = hotel.find_element(By.XPATH, './/a[contains(@class, "l1ovpqvx")]').get_attribute('href')
                location = clean_text(hotel.find_element(By.XPATH, './/div[contains(@class, "fb4nyux")]//span[contains(@class, "t6mzqp7")]').text)
                total_price = clean_text(hotel.find_element(By.XPATH, '//div[@class="_tt122m"]').text)
                rating_reviews = clean_text(hotel.find_element(By.XPATH, './/span[contains(@class, "r4a59j5")]/span[@aria-hidden="true"]').text)
                tag_text = clean_text(hotel.find_element(By.XPATH, '//div[@class="t1qa5xaj dir dir-ltr"]').text)

                hotel_info = {
                    "image_url": image_url,
                    "hotel_name": hotel_name,
                    "payment_url": payment_url,
                    "location": location,
                    "total_price": total_price,
                    "rating_reviews": rating_reviews,
                    "tag_text": tag_text,
                }
                
                hotels_data.append(hotel_info)
            except Exception as e:
                print(f"Error extracting data for a hotel: {e}")

    extract_hotels()
    driver.quit()
    
    response_dict = {
        'type': 'airbnb',
        'data': hotels_data
    }
    
    return response_dict

# Example usage
if __name__ == "__main__":
    data = scrape_airbnb("goa", "2025-02-09", "2025-02-14", "1", "0")
    print(json.dumps(data, indent=2))
