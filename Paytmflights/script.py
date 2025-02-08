from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
import http  # only used in the sendString function below if needed

def generate_paytm_flight_url(origin_code, origin_name, dest_code, dest_name, 
                               adults, children, infants, class_type, 
                               departure_date, referer='home'):
    base_url = "https://tickets.paytm.com/flights/flightSearch"
    return f"{base_url}/{origin_code}-{origin_name}/{dest_code}-{dest_name}/{adults}/{children}/{infants}/{class_type}/{departure_date}?referer={referer}"

def get_booking_url(driver, flight_id):
    try:
        initial_url = driver.current_url
        flight_container = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, flight_id))
        )
        ActionChains(driver).move_to_element(flight_container).perform()
        time.sleep(1)

        view_fare_btn = WebDriverWait(flight_container, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.zHp8j'))
        )
        
        for click_method in [lambda: view_fare_btn.click(),
                             lambda: driver.execute_script("arguments[0].click();", view_fare_btn),
                             lambda: ActionChains(driver).move_to_element(view_fare_btn).click().perform()]:
            try:
                click_method()
                break
            except:
                continue
        
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div._2Gvo0'))
        )

        proceed_selectors = [
            (By.XPATH, "//button[contains(., 'Proceed')]")
        ]

        proceed_btn = None
        for selector in proceed_selectors:
            try:
                proceed_btn = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(selector)
                )
                break
            except:
                continue

        if not proceed_btn:
            raise Exception("All proceed button selectors failed")

        original_window = driver.current_window_handle
        ActionChains(driver).move_to_element(proceed_btn).pause(0.5).click().perform()
        
        WebDriverWait(driver, 1).until(EC.number_of_windows_to_be(2))
        new_window = [window for window in driver.window_handles if window != original_window][0]
        driver.switch_to.window(new_window)
        booking_url = driver.current_url
        driver.close()
        driver.switch_to.window(original_window)
        
        return booking_url
    except:
        driver.save_screenshot('error.png')
        return None

def scrape_flights(url, paseenger_count):
    driver = webdriver.Chrome()
    driver.get(url)
    flights_data = []
    
    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pIInI')))
        
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        flight_containers = driver.find_elements(By.CSS_SELECTOR, 'div.pIInI')
        
        for container in flight_containers:
            try:
                flight_id = container.find_element(By.CSS_SELECTOR, 'div._3VUCr').get_attribute('id')
                airline = container.find_element(By.CLASS_NAME, '_2cP56').text
                airline_logo = container.find_element(By.TAG_NAME, 'img').get_attribute('src')
                
                time_sections = container.find_elements(By.CLASS_NAME, '_29g4q')
                departure_time = time_sections[0].find_element(By.CLASS_NAME, '_3gpc5').text.replace('\n', '')
                departure_city = time_sections[0].find_element(By.CLASS_NAME, 'TpcIu').text
                arrival_time = time_sections[1].find_element(By.CLASS_NAME, '_3gpc5').text.replace('\n', '')
                arrival_city = time_sections[1].find_element(By.CLASS_NAME, 'TpcIu').text
                
                duration_element = container.find_element(By.CLASS_NAME, '_1J4f_')
                duration_text = duration_element.text
                layover = 0  
                
                if '•' in duration_text:
                    parts = [part.strip() for part in duration_text.split('•')]
                    if len(parts) > 1 and 'Non-Stop' not in parts[1]:
                        layover = 1
                
                price = container.find_element(By.CLASS_NAME, '_2MkSl').text.replace('₹', '').replace(',', '')
                fare_type = container.find_element(By.CLASS_NAME, '_25oBA').text
                offer = container.find_element(By.CLASS_NAME, '_1LjFU').text if container.find_elements(By.CLASS_NAME, '_1LjFU') else ''
                
                flights_data.append({
                    'flight_id': flight_id,
                    'airline': airline,
                    'airline_logo': airline_logo,
                    'departure_time': departure_time,
                    'departure_city': departure_city,
                    'arrival_time': arrival_time,
                    'arrival_city': arrival_city,
                    'duration': duration_text,
                    'price': paseenger_count * int(price),
                    'fare_type': fare_type,
                    'offer': offer,
                    'layover': layover,
                    'url' : get_booking_url(driver, flight_id)
                })
                
                # Limit to 10 flights
                if len(flights_data) >= 10:
                    break
                
            except Exception as e:
                continue
                
        with open('flights_data.json', 'w') as f:
            json.dump(flights_data, f, indent=2)
            
        return driver
    except Exception as e:
        driver.quit()
        return None


if __name__ == "__main__":
    url = generate_paytm_flight_url("BLR", "Bengaluru", "DED", "Dehradun", 1, 1, 0, 'E', departure_date="2025-02-04")
    paseenger_count = 2
    driver = scrape_flights(url, paseenger_count)
    
    driver.quit()
