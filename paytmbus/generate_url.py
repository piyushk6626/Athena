"""
Paytm Bus URL Generator and Data Scraper Module

This module provides functionality to generate Paytm bus booking URLs and scrape bus information
from Paytm's bus booking platform. It uses Selenium WebDriver to automate the process of
extracting bus details including prices, schedules, and availability.

Classes:
    None

Functions:
    get_bus_data(url: str, limit: int = 10) -> str: Scrapes bus information from a given Paytm URL
    generate_paytm_bus_url(source: str, destination: str, journey_date: str) -> dict: Generates URL and returns bus data

Dependencies:
    - selenium: For web automation
    - json: For data serialization
    - datetime: For date validation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .xpath import *
import json


def get_bus_data(url: str, limit: int = 10) -> str:
    """
    Scrapes bus information from a given Paytm URL.

    This function uses Selenium WebDriver to automate the process of extracting bus details
    from Paytm's bus booking platform. It waits for the page to load and then extracts
    information such as bus name, type, schedule, price, and availability.

    Args:
        url (str): The Paytm bus search URL to scrape
        limit (int, optional): Maximum number of bus results to return. Defaults to 10.

    Returns:
        str: JSON string containing a list of dictionaries with bus information

    Note:
        The function uses headless Chrome browser for scraping.
        It includes error handling for cases where certain information might not be available.
    """
    # Configure Chrome options for headless operation
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the main container of bus cards to load (timeout: 15 seconds)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.XPATH, cards_xpath)))

    buses = []
    # Get the specified number of bus cards
    cards = driver.find_elements(By.XPATH, cards_xpath)[:limit]

    for card in cards:
        try:
            # Extract basic bus information
            bus_name = card.find_element((By.XPATH, bus_name_xpath)).text
            bus_type = card.find_element(By.XPATH, bus_type_xpath).text
            departure_time = card.find_element(By.XPATH, departure_time_xpath).text
            departure_date = card.find_element(By.XPATH, departure_date_xpath).text
            arrival_time = card.find_element(By.XPATH, arrival_time_xpath).text
            arrival_date = card.find_element(By.XPATH, arrival_date_xpath).text
            duration = card.find_element(By.XPATH, duration_xpath).text

            # Extract price with error handling
            try:
                final_price_element = card.find_element(By.XPATH,final_price_xpath)
                final_price = final_price_element.text[1:]  # Remove currency symbol
            except:
                final_price = "N/A"

            # Extract rating with error handling
            try:
                rating = card.find_element(By.XPATH, rating_xpath).text
            except:
                rating = "N/A"

            # Extract seats available with error handling
            try:
                seats_available = card.find_element(By.XPATH, seats_available_xpath).text.split()[0]
            except:
                seats_available = "N/A"

            # Create bus information dictionary
            bus_info = {
                "bus_name": bus_name,
                "bus_type": bus_type,
                "departure_time": departure_time,
                "departure_date": departure_date,
                "arrival_time": arrival_time,
                "arrival_date": arrival_date,
                "duration": duration,
                "final_price": final_price,
                "rating": rating,
                "seats_available": seats_available,
                "url": url
            }
            buses.append(bus_info)
        except Exception as e:
            print(f"Error extracting data for a bus: {e}")

    driver.quit()
    return json.dumps(buses, indent=4)


def generate_paytm_bus_url(source: str, destination: str, journey_date: str) -> dict:
    """
    Generate a Paytm Bus URL and return the scraped data.

    This function creates a valid Paytm bus search URL and retrieves bus information
    for the specified route and date. It includes input validation and proper error handling.

    Args:
        source (str): Source city name. The first letter of the city name is capitalized.
        destination (str): Destination city name. The first letter of the city name is capitalized.
        journey_date (str): Date of journey in the format YYYY-MM-DD.

    Returns:
        dict: A dictionary containing either:
            - Bus data in JSON format if successful
            - Error message if date format is invalid or no buses are found

    Raises:
        ValueError: If the date format is invalid.

    Example:
        >>> generate_paytm_bus_url("Bangalore", "Pune", "2025-03-01")
        {'type': 'bus', 'data': [...]}
    """
    from datetime import datetime
    
    try:
        # Validate date format
        datetime.strptime(journey_date, "%Y-%m-%d")
        
        # Capitalize city names for URL formatting
        source = source.capitalize()
        destination = destination.capitalize()
        
        # Construct the Paytm bus search URL
        url = f"https://tickets.paytm.com/bus/search/{source}/{destination}/{journey_date}/1"

        try:
            # Attempt to scrape bus data
            data = get_bus_data(url)
        except:
            data = None
        
        # Prepare response based on data availability
        if data:
            response_dict = {
                'type': 'bus',
                'data': data
            }
        else:
            response_dict = {
                'type': 'text',
                'data': "No buses found."
            }

        return response_dict
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."


if __name__ == "__main__":
    # Example usage
    source = "Bangalore"
    destination = "Pune"
    journey_date = "2025-03-01"
    
    print(generate_paytm_bus_url(source, destination, journey_date))
    