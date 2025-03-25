from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from .xpaths import *
# Load airport codes from JSON file
def load_airport_codes():
    """Loads airport codes from a JSON file. If the file does not exist, prints
    a FileNotFoundError message and returns an empty dictionary. If the JSON
    file is malformed, prints a JSONDecodeError message and returns an empty
    dictionary. Otherwise returns a dictionary mapping airport names to their
    respective IATA codes."""
    try:
        with open('flightCompare/airport_codes.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Airport codes JSON file not found")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON file")
        return {}

def search_flight_url(source, destination, date):
    # Load airport codes from JSON file
    """
    Constructs a search URL for flights and initiates scraping.

    Args:
        source (str): The departure city name.
        destination (str): The arrival city name.
        date (str): The date of travel in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary with scraped flight data.
    """

    airport_codes = load_airport_codes()
    
    url = f"https://www.in.cheapflights.com/flight-search/{airport_codes.get(source)}-{airport_codes.get(destination)}/{date}?ucs=12mksjb"
    
    return scrape_flights(url, source, destination)
    



def scrape_flights(url: str, origin: str, destination: str) -> dict:
    """
    Scrapes flights from a given URL, origin and destination.

    Args:
        url (str): The URL to scrape.
        origin (str): The origin city.
        destination (str): The destination city.

    Returns:
        dict: A dictionary with the scraped flight data.
    """
    # Set up Chrome options for browser
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL in browser
    driver.get(url)

    try:
        # Wait for the flight results to load (max 20 seconds)
        wait = WebDriverWait(driver, 20)
        flight_containers = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, FLIGHT_CONTAINER)  # Using XPath constant from xpaths.py
        ))

        flights_data = []

        # Iterate through each flight container to extract details
        for container in flight_containers:
            try:
                # Extract basic flight information using XPath constants
                departure_info = container.find_element(By.XPATH, DEPARTURE_INFO).text
                arrival_info = container.find_element(By.XPATH, ARRIVAL_INFO).text
                price_text = container.find_element(By.XPATH, PRICE_TEXT).text
                duration = container.find_element(By.XPATH, DURATION).text
                stops = container.find_element(By.XPATH, STOPS).text
                img_element = container.find_element(By.XPATH, IMG_ELEMENT)
                booking_link = container.find_element(By.XPATH, BOOKING_LINK)

                # Extract provider details (usually shows different booking options)
                provider_links = container.find_elements(By.XPATH, PROVIDER_LINKS)
                provider1_name = provider1_price = provider1_url = ""
                provider2_name = provider2_price = provider2_url = ""

                # Extract first provider details if available
                if len(provider_links) >= 1:
                    try:
                        provider1 = provider_links[0]
                        provider1_url = provider1.get_attribute('href')
                        provider1_price = provider1.find_element(By.XPATH, PROVIDER_PRICE).text
                        provider1_name = provider1.find_element(By.XPATH, PROVIDER_NAME).text
                    except Exception as e:
                        print(f"Error scraping provider1 details: {str(e)}")

                # Extract second provider details if available
                if len(provider_links) >= 2:
                    try:
                        provider2 = provider_links[1]
                        provider2_url = provider2.get_attribute('href')
                        provider2_price = provider2.find_element(By.XPATH, PROVIDER_PRICE).text
                        provider2_name = provider2.find_element(By.XPATH, PROVIDER_NAME).text
                    except Exception as e:
                        print(f"Error scraping provider2 details: {str(e)}")

                # Create a dictionary with all flight information
                flight_data = {
                    'provider': 'Cheapflights',
                    'airline': img_element.get_attribute('alt'),
                    'airline_logo': img_element.get_attribute('src'),
                    'departure_time': departure_info,
                    'departure_city': origin,
                    'arrival_time': arrival_info,
                    'arrival_city': destination,
                    'duration': duration,
                    'price': price_text,
                    'fare_type': 'Economy',  # Default value as website doesn't provide this info
                    'offer': '',             # Empty as website doesn't provide offers
                    'layover': stops,
                    'url': booking_link.get_attribute('href'),
                    'provider1_name': provider1_name,
                    'provider1_price': provider1_price,
                    'provider1_url': provider1_url,
                    'provider2_name': provider2_name,
                    'provider2_price': provider2_price,
                    'provider2_url': provider2_url
                }

                flights_data.append(flight_data)

            except Exception as e:
                print(f"Error scraping flight details: {str(e)}")
                continue

        # Return the final results
        result = {
            "type": "flightCompare",
            "data": flights_data
        }
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"type": "text", "data": ["No flights found"]}

if __name__ == "__main__":
    results = search_flight_url("Bangalore", "Mumbai", "2025-03-03")
    
    print(results)

