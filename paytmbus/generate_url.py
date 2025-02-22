# URL: tickets.paytm.com.com/bus/search/{SOURCE}/{DESTINATION}/{JOURNEY-DATE}/1?URL
# DATE_FORMAT: YYYY-MM-DD
# SOURCE: First letter of city is capital
# DESTINATION: First letter of city is capital

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .xpath import *
import json


def get_bus_data(url: str, limit: int = 10):
    options = Options()
    options.add_argument("--headless")
    # service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome( options=options)
    driver.get(url)

    # Explicit wait for the main container of bus cards to load
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.XPATH, cards_xpath)))

    buses = []
    cards = driver.find_elements(By.XPATH, cards_xpath)[:limit]

    for card in cards:
        try:
            bus_name = wait.until(EC.presence_of_element_located((By.XPATH, bus_name_xpath))).text
            bus_type = card.find_element(By.XPATH, bus_type_xpath).text
            departure_time = card.find_element(By.XPATH, departure_time_xpath).text
            departure_date = card.find_element(By.XPATH, departure_date_xpath).text
            arrival_time = card.find_element(By.XPATH, arrival_time_xpath).text
            arrival_date = card.find_element(By.XPATH, arrival_date_xpath).text
            duration = card.find_element(By.XPATH, duration_xpath).text

            try:
                final_price_element = card.find_element(By.XPATH,final_price_xpath)
                final_price = final_price_element.text[1:]
            except:
                final_price = "N/A"

            try:
                rating = card.find_element(By.XPATH, rating_xpath).text
            except:
                rating = "N/A"

            try:
                seats_available = card.find_element(By.XPATH, seats_available_xpath).text.split()[0]
            except:
                seats_available = "N/A"

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



def generate_paytm_bus_url(source, destination, journey_date):
    """
    Generate a Paytm Bus URL and return the scraped data.

    Args:
        source (str): Source city name. The first letter of the city name is capitalized.
        destination (str): Destination city name. The first letter of the city name is capitalized.
        journey_date (str): Date of journey in the format YYYY-MM-DD.

    Returns:
        dict: A dictionary containing the scraped data.

    Raises:
        ValueError: If the date format is invalid.
    """
    from datetime import datetime
    
    try:
        datetime.strptime(journey_date, "%Y-%m-%d")
        
        source = source.capitalize()
        destination = destination.capitalize()
        
        url = f"https://tickets.paytm.com/bus/search/{source}/{destination}/{journey_date}/1"

        try:
            data = get_bus_data(url)
        except:
            data = None
        
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
    source = "Bangalore"
    destination = "Pune"
    journey_date = "2025-03-01"
    
    print(generate_paytm_bus_url(source, destination, journey_date))
    