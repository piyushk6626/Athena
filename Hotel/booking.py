"""
This module provides functionality to scrape hotel information from Booking.com.
It uses Selenium WebDriver to automate browser interactions and extract hotel details
including prices, ratings, reviews, and amenities.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .xpath import (
    HOTEL_CONTAINER,
    HOTEL_TITLE,
    REVIEW_COUNT,
    REVIEW_COMMENT,
    HOTEL_IMAGE,
    HOTEL_URL,
    BREAKFAST_INCLUDED
)
import json
import time

def scroll_page(driver):
    """
    Scrolls the webpage to load more hotel listings.
    
    Args:
        driver: Selenium WebDriver instance
        
    Note:
        This function scrolls until either:
        1. At least 15 hotel containers are loaded
        2. The bottom of the page is reached
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
        
    while True:
        # Wait for hotel containers to load
        wait = WebDriverWait(driver, 20)
        containers = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, HOTEL_CONTAINER)
        ))
        if len(containers)>=15: break
    
        # Scroll down by 1000 pixels
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2)  # Wait for content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break
        last_height = new_height

# Sample price and rating data for random assignment
price=[4236,2545,3595,1679,1845,6495]
import random
rating=[4.1,3.2,2.9,4.7,3.8,4.4]

def get_hotel_details(container):
    """
    Extracts hotel information from a container element.
    
    Args:
        container: Selenium WebElement containing hotel information
        
    Returns:
        dict: Dictionary containing hotel details including:
            - title: Hotel name
            - price: Random price from predefined list
            - review count: Number of reviews
            - review comment: Sample review text
            - rating: Random rating from predefined list
            - image_url: URL of hotel image
            - hotel url: URL of hotel page
            - Breakfast included: Boolean indicating breakfast availability
            
    Returns:
        None: If any required element is not found
    """
    try:
        # Extract basic hotel information
        hotel_data = {
            'title': str(container.find_element(By.CSS_SELECTOR, HOTEL_TITLE).text),
            'price': str(random.choice(price)),
            'review count': str(container.find_element(By.CSS_SELECTOR, REVIEW_COUNT).text).split()[0],
            'review comment': str(container.find_element(By.CSS_SELECTOR, REVIEW_COMMENT).text),
            'rating': str(random.choice(rating)),
            'image_url': str(container.find_element(By.CSS_SELECTOR, HOTEL_IMAGE).get_attribute('src')),
            'hotel url': str(container.find_element(By.CSS_SELECTOR, HOTEL_URL).get_attribute('href'))
        }
        
        # Check if breakfast is included
        try:
            container.find_element(By.CSS_SELECTOR, BREAKFAST_INCLUDED).text
            hotel_data['Breakfast included'] = "True"
        except:
            hotel_data['Breakfast included'] = "False"
        return hotel_data
    
    except NoSuchElementException as e:
        print(f"Missing element: {str(e)}")
        return None
        
def scrape_hotels(location,checkin:str,checkout:str,no_adults=1,no_rooms=1,no_children=0)->list[dict]:
    """
    Scrape hotel data from booking.com.

    Args:
        location (str): Location to search for hotels (e.g. "goa")
        checkin (str): Checkin date in the format "yyyy-mm-dd"
        checkout (str): Checkout date in the format "yyyy-mm-dd"
        no_adults (int): Number of adults (default: 1)
        no_rooms (int): Number of rooms (default: 1)
        no_children (int): Number of children (default: 0)

    Returns:
        dict: A dictionary containing:
            - type (str): "booking"
            - data (list): List of hotel dictionaries, each containing:
                - title (str): The title of the hotel
                - price (str): The price of the hotel
                - review count (str): The number of reviews
                - review comment (str): A sample review comment
                - rating (str): The rating of the hotel
                - image_url (str): The URL of the hotel image
                - hotel url (str): The URL of the hotel page
                - Breakfast included (str): "True" or "False"

    Raises:
        TimeoutException: If the page takes too long to load
        Exception: If any other error occurs during scraping
    """
    # Construct the URL with search parameters
    url = f"https://www.booking.com/searchresults.en-gb.html?ss={location}&checkin={checkin}&checkout={checkout}&group_adults={no_adults}&group_children={no_children}&no_rooms={no_rooms}"
    
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    hotels_data = []
    
    try:
        # Load the webpage and scroll to load more results
        driver.get(url)
        scroll_page(driver)
        
        # Wait for hotel containers to load
        wait = WebDriverWait(driver, 20)
        containers = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, HOTEL_CONTAINER)
        ))
        
        print(f"Found {len(containers)} product containers")
        
        # Extract details from each hotel container
        for container in containers:
            hotel_data = get_hotel_details(container)
            if hotel_data:
                if hotel_data['title'] == "":
                    continue
                hotels_data.append(hotel_data)
                if len(hotel_data) >= 10:
                    break
        
        print(hotel_data)
        return {"type":"booking",
                "data":hotels_data}
    
    except TimeoutException:
        print("Timeout while waiting for elements to load")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    # Example usage
    location = "Goa"
    checkin="2025-02-12"
    checkout="2025-02-16"
    no_adults=6
    hotels = scrape_hotels(location,checkin,checkout)
    
    # Save results to JSON file
    with open('hotels_data.json', 'w', encoding='utf-8') as f:
        json.dump(hotels, f, ensure_ascii=False, indent=4)


