from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Navigate to the URL
url = "https://in.bookmyshow.com/buytickets/sky-force-pune/movie-pune-ET00371539-MT/20250130#"
driver.get(url)

def scroll_page(driver):
    """Scroll the page to load all dynamic JavaScript content"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    while True:
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break

# Scroll to ensure all data is loaded
scroll_page(driver)

time.sleep(5)  # Allow content to load

# Extract theater data
theaters = driver.find_elements(By.XPATH, "//li[@class='list' and @data-lat]")

output_data = []

for theater in theaters:
    try:
        lat = theater.get_attribute("data-lat")
        lng = theater.get_attribute("data-lng")
        name = theater.get_attribute("data-name")
        showtimes = theater.find_elements(By.XPATH, ".//div[@class='showtime-pill-container _available']/a")
        
        shows = []
        for showtime in showtimes:
            show_data = {
                "href": showtime.get_attribute("href"),
                "session_id": showtime.get_attribute("data-session-id"),
                "showtime_code": showtime.get_attribute("data-showtime-code"),
                "showtime_filter_index": showtime.get_attribute("data-showtime-filter-index"),
                "date_time": showtime.get_attribute("data-date-time"),
                "display_showtime": showtime.get_attribute("data-display-showtime"),
                "is_atmos_enabled": showtime.get_attribute("data-is-atmos-enabled"),
                "availability": showtime.get_attribute("data-availability"),
                "cut_off_date_time": showtime.get_attribute("data-cut-off-date-time"),
                "venue_code": showtime.get_attribute("data-venue-code"),
                "event_id": showtime.get_attribute("data-event-id"),
                "attributes": showtime.get_attribute("data-attributes"),
                "overall_avail_status": showtime.get_attribute("data-overall-avail-status"),
                "categories": showtime.get_attribute("data-categories"),
                "category_popup": showtime.get_attribute("data-cat-popup")
            }
            shows.append(show_data)
        
        output_data.append({
            "latitude": lat,
            "longitude": lng,
            "name": name,
            "showtimes": shows
        })
    except Exception as e:
        print(f"Error extracting data: {e}")

# Save output to JSON file
with open("bookmyshow_data.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

print("Data extraction complete. JSON saved.")

driver.quit()


