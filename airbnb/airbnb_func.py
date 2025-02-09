from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from urllib.parse import urlparse, parse_qs

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
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Automatically manage ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.airbnb.co.in/s/{destination}/homes?checkin={checkinDate}&checkout={checkoutDate}&adults={adultsNo}&children={childrenNo}&query={destination}"
    
    driver.get(url)
    time.sleep(5)  # Wait for the page to load
    
    hotels_data = []
    
    def extract_hotels():
        hotels = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
        
        for hotel in hotels:
            try:
                images = [img.get_attribute('src') for img in hotel.find_elements(By.XPATH, './/div/picture/img')]
                hotel_name = hotel.find_element(By.XPATH, './/div[contains(@class, "t1jojoys")]').text
                hotel_url = hotel.find_element(By.XPATH, './/a[contains(@class, "l1ovpqvx")]').get_attribute('href')
                location_details = hotel.find_element(By.XPATH, './/div[contains(@class, "g1qv1ctd")]').text
                price = hotel.find_element(By.XPATH, './/div[contains(@class, "pquyp1l")]').text
                total_price = driver.find_element(By.XPATH, '//div[@class="_tt122m"]').text
                ratings = hotel.find_element(By.XPATH, './/span[contains(@class, "r4a59j5")]/span[@aria-hidden="true"]').text
                room_tag = driver.find_element(By.XPATH, '//div[@class="t1qa5xaj dir dir-ltr"]').text
                payment_link = driver.find_element(By.XPATH, '//div/a[@class="l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 bn2bl2p atm_5j_223wjw atm_9s_1ulexfb atm_e2_1osqo2v atm_fq_idpfg4 atm_mk_stnw88 atm_tk_idpfg4 atm_vy_1osqo2v atm_26_1j28jx2 atm_3f_glywfm atm_kd_glywfm atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_aaiy6o_1w3cfyq_oggzyc atm_70_1b8lkes_1w3cfyq_oggzyc atm_uc_glywfm_1w3cfyq_pynvjw atm_uc_aaiy6o_pfnrn2_ivgyl9 atm_70_1b8lkes_pfnrn2_ivgyl9 atm_uc_glywfm_pfnrn2_61fwbc dir dir-ltr"]').get_attribute("href")
                
                hotel_info = {
                    "image_url": images[0],
                    "hotel_name": hotel_name,
                    "hotel_url": hotel_url,
                    "location": location_details,
                    
                    "total_price": total_price,
                    "rating_reviews": ratings,
                    "tag_text": room_tag,
                    "payment_url": payment_link,
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
