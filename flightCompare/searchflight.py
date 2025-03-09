# https://www.in.cheapflights.com/flight-search/BOM-BLR/2025-03-11?ucs=12mksjb


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .airportCode import INDIAN_AIRPORT_CODES



def search_flight_url(source, destination, date):
    url = f"https://www.in.cheapflights.com/flight-search/{INDIAN_AIRPORT_CODES[source]}-{INDIAN_AIRPORT_CODES[destination]}/{date}?ucs=12mksjb"
    print(url)
    return scrape_flights(url,source,destination)
    



def scrape_flights(url, origin, destination):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    driver.get(url)

    try:
        # Wait for the flight results to load
        wait = WebDriverWait(driver, 20)
        flight_containers = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="Fxw9-result-item-container"]/div[@class="nrc6 nrc6-mod-pres-default nrc6-mod-desktop-responsive"]')
        ))

        flights_data = []

        for container in flight_containers:
            try:
                # Extract flight details
                departure_info = container.find_element(By.XPATH, '(.//div[@class="vmXl vmXl-mod-variant-large"]/span)[1]').text
                arrival_info = container.find_element(By.XPATH, '(.//div[@class="vmXl vmXl-mod-variant-large"]/span)[3]').text
                price_text = container.find_element(By.XPATH, './/div[@class="f8F1-price-text-container"]/div[@class="f8F1-price-text"]').text
                duration = container.find_element(By.XPATH, './/div[@class="xdW8 xdW8-mod-full-airport"]/div[@class="vmXl vmXl-mod-variant-default"]').text
                stops = container.find_element(By.XPATH, './/span[@class="JWEO-stops-text"]').text
                img_element = container.find_element(By.XPATH, './/img')
                booking_link = container.find_element(By.XPATH, './/a[@role="link" and contains(@class, "Iqt3")]')

                # Extract the first two provider links and flatten the data
                provider_links = container.find_elements(By.XPATH, './/a[@class="oVHK-fclink"]')
                provider1_name = provider1_price = provider1_url = ""
                provider2_name = provider2_price = provider2_url = ""

                if len(provider_links) >= 1:
                    try:
                        provider1 = provider_links[0]
                        provider1_url = provider1.get_attribute('href')
                        provider1_price = provider1.find_element(
                            By.XPATH, './/div[@class="c_f8N-link-wrapper"]/span[@class="c_f8N-price"]/span'
                        ).text
                        provider1_name = provider1.find_element(
                            By.XPATH, './/div[@class="c_f8N-link-wrapper"]/span[@class="c_f8N-provider"]'
                        ).text
                    except Exception as e:
                        print(f"Error scraping provider1 details: {str(e)}")
                if len(provider_links) >= 2:
                    try:
                        provider2 = provider_links[1]
                        provider2_url = provider2.get_attribute('href')
                        provider2_price = provider2.find_element(
                            By.XPATH, './/div[@class="c_f8N-link-wrapper"]/span[@class="c_f8N-price"]/span'
                        ).text
                        provider2_name = provider2.find_element(
                            By.XPATH, './/div[@class="c_f8N-link-wrapper"]/span[@class="c_f8N-provider"]'
                        ).text
                    except Exception as e:
                        print(f"Error scraping provider2 details: {str(e)}")

                # Build a flattened flight data dictionary with provider details at the top level
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
                    'fare_type': 'Economy',  # Default as not provided
                    'offer': '',             # Empty as not provided
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

        result = {
            "type": "flightCompare",
            "data": flights_data
        }
        return result

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"type": "text", "data": ["No flights found"]}

    finally:
        driver.quit()

if __name__ == "__main__":
    results = search_flight_url("Bangalore", "Mumbai", "2025-03-03")
    
    print(results)

