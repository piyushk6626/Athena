from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def get_bus_data(url: str, limit: int = 10):
    options = Options()
    options.add_argument("--headless")
    # service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome( options=options)
    driver.get(url)

    # Explicit wait for the main container of bus cards to load
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='IHKeM']")))

    buses = []
    cards = driver.find_elements(By.XPATH, "//div[@class='IHKeM']")[:limit]

    for card in cards:
        try:
            bus_name = wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='+iUf5']"))).text
            bus_type = card.find_element(By.XPATH, ".//div[@class='G88l9']").text
            departure_time = card.find_element(By.XPATH, ".//div[@class='wYtCy']//div[@class='_4rWgi']").text
            departure_date = card.find_element(By.XPATH, ".//div[@class='wYtCy']//div[@class='C3vrs']").text
            arrival_time = card.find_element(By.XPATH, ".//div[@class='EjC2U']//div[@class='_4rWgi']").text
            arrival_date = card.find_element(By.XPATH, ".//div[@class='EjC2U']//div[@class='C3vrs']").text
            duration = card.find_element(By.XPATH, ".//div[@class='_1D2hF']").text

            try:
                final_price_element = card.find_element(By.XPATH, ".//span[@class='A2eT9 F+C81']")
                final_price = final_price_element.text[1:]
            except:
                final_price = "N/A"

            try:
                rating = card.find_element(By.XPATH, ".//div[@class='eoyaT']/div").text
            except:
                rating = "N/A"

            try:
                seats_available = card.find_element(By.XPATH, ".//div[@class='UxGbP'][1]").text.split()[0]
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

if __name__ == "__main__":
    url = input("Enter the URL: ")
    bus_data = get_bus_data(url)
    print(bus_data)
