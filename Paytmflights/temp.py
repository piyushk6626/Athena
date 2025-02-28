from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
import http  # only used in the sendString function below if needed

# https://tickets.paytm.com/flights/flightSearch/BLR-Bangalore/PNQ-Pune/2025-03-04/1/0/0/2025-02-25
# https://tickets.paytm.com/flights/flightSearch/DEL-Delhi/BOM-Mumbai/1/0/0/E/2025-02-25?referer=home
def generate_paytm_flight_url(origin_codeu, origin_nameu, dest_codeu, dest_nameu, 
                               adultsu, childrenu, infantsu, class_typeu, 
                               departure_dateu, refereru='home'):
    base_url = "https://tickets.paytm.com/flights/flightSearch"
    return f"{base_url}/{origin_codeu}-{origin_nameu}/{dest_codeu}-{dest_nameu}/{adultsu}/{childrenu}/{infantsu}/{class_typeu}/{departure_dateu}?refereru={refereru}"

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


import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Mapping of major Indian airports (city to IATA code)
INDIAN_AIRPORT_CODES = {
    "Mumbai": "BOM",
    "Delhi": "DEL",
    "Bangalore": "BLR",
    "Bengaluru": "BLR",
    "Hyderabad": "HYD",
    "Chennai": "MAA",
    "Kolkata": "CCU",
    "Ahmedabad": "AMD",
    "Pune": "PNQ",
    "Jaipur": "JAI",
    "Lucknow": "LKO",
    "Goa": "GOI",
    "Kochi": "COK",
    "Thiruvananthapuram": "TRV",
    "Coimbatore": "CJB",
    "Guwahati": "GAU",
    "Patna": "PAT",
    "Nagpur": "NAG",
    "Indore": "IDR",
    "Bhopal": "BHO",
    "Visakhapatnam": "VTZ",
    "Varanasi": "VNS",
    "Amritsar": "ATQ",
    "Srinagar": "SXR",
    "Chandigarh": "IXC",
    "Ranchi": "IXR",
    "Bhubaneswar": "BBI",
    "Tiruchirappalli": "TRZ",
    "Madurai": "IXM",
    "Raipur": "RPR",
    "Surat": "STV",
    "Imphal": "IMF",
    "Agartala": "IXA",
    "Dehradun": "DED",
    "Port Blair": "IXZ",
    "Leh": "IXL",
    "Shillong": "SHL",
    "Dibrugarh": "DIB",
    "Jodhpur": "JDH",
    "Udaipur": "UDR",
    "Vadodara": "BDQ",
    "Rajkot": "RAJ",
    "Bhavnagar": "BHU",
    "Jamnagar": "JGA",
    "Kannur": "CNN",
    "Mangalore": "IXE",
    "Belgaum": "IXG",
    "Hubli": "HBX",
    "Tirupati": "TIR",
    "Vijayawada": "VGA",
    "Rajahmundry": "RJA",
    "Kadapa": "CDP",
    "Aurangabad": "IXU",
    "Nashik": "ISK",
    "Kolhapur": "KLH",
    "Solapur": "SSE",
    "Jabalpur": "JLR",
    "Gwalior": "GWL",
    "Allahabad": "IXD",
    "Gorakhpur": "GOP",
    "Bareilly": "BEK",
    "Kanpur": "KNU",
    "Jhansi": "JHS",
    "Dharamsala": "DHM",
    "Kullu": "KUU",
    "Shimla": "SLV",
    "Kangra": "DHM",
    "Bhuj": "BHJ",
    "Kandla": "IXY",
    "Porbandar": "PBD",
    "Bhavnagar": "BHU",
    "Diu": "DIU",
    "Silchar": "IXS",
    "Dimapur": "DMU",
    "Aizawl": "AJL",
    "Lilabari": "IXI",
    "Tezpur": "TEZ",
    "Jorhat": "JRH",
    "North Lakhimpur": "IXI",
    "Pasighat": "IXT",
    "Along": "IXV",
    "Zero": "ZER",
    "Itanagar": "HGI",
    "Daporijo": "DEP",
    "Tezu": "TEI",
    "Rupsi": "RUP",
    "Cooch Behar": "COH",
    "Malda": "LDA",
    "Balurghat": "RGH",
    "Barrackpore": "BQP",
    "Behala": "BHP",
    "Bhubaneswar": "BBI",
    "Jamshedpur": "IXW",
    "Rourkela": "RRK",
    "Bokaro": "BKR",
    "Gaya": "GAY",
    "Muzaffarpur": "MZU",
    "Darbhanga": "DBR",
    "Purnea": "PUI",
    "Bagdogra": "IXB",
    "Gorakhpur": "GOP",
    "Kanpur": "KNU",
    "Allahabad": "IXD",
    "Agra": "AGR",
    "Jaisalmer": "JSA",
    "Jhansi": "JHS",
    "Khajuraho": "HJR",
    "Bikaner": "BKB",
    "Kota": "KTU",
    "Udaipur": "UDR",
    "Jodhpur": "JDH",
    "Ajmer": "AJM",
    "Alwar": "AJL",
    "Bhilwara": "BHL",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Dungarpur": "DUN",
    "Hanumangarh": "HNM",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR",
    "Banswara": "BAN",
    "Barmer": "BMR",
    "Bharatpur": "BHR",
    "Bhilwara": "BHL",
    "Bikaner": "BKB",
    "Bundi": "BDI",
    "Chittorgarh": "CIT",
    "Churu": "CUR",
    "Dausa": "DAU",
    "Dholpur": "DHL",
    "Dungarpur": "DUN",
    "Ganganagar": "GGR",
    "Hanumangarh": "HNM",
    "Jaipur": "JAI",
    "Jaisalmer": "JSA",
    "Jalore": "JAL",
    "Jhalawar": "JHL",
    "Jhunjhunu": "JHJ",
    "Jodhpur": "JDH",
    "Karauli": "KAR",
    "Kota": "KTU",
    "Nagaur": "NGR",
    "Pali": "PLI",
    "Pratapgarh": "PRG",
    "Rajsamand": "RJM",
    "Sawai Madhopur": "SWM",
    "Sikar": "SIK",
    "Sirohi": "SIH",
    "Tonk": "TNK",
    "Udaipur": "UDR"
}

def get_airport_code(city_name):
    """Returns the IATA airport code for a given city name."""
    return INDIAN_AIRPORT_CODES.get(city_name, None)

def scrape_flights(origin_name, dest_name, departure_date):
    time.sleep(2)
    """
    Scrapes flight data from Paytm given origin and destination names, departure date.
    Defaults to one adult in economy class.
    
    Parameters:
    -----------
    origin_name : str
        Name of the departure city.
    dest_name : str
        Name of the destination city.
    departure_date : str
        Date of departure in 'YYYY-MM-DD' format.
    
    Returns:
    --------
    Dictionary with flight data.
    """
    origin_code = INDIAN_AIRPORT_CODES[origin_name]
    dest_code = INDIAN_AIRPORT_CODES[dest_name]

    if not origin_code or not dest_code:
        return {"error": "Invalid origin or destination city. Please check the inputs."}

    # Default parameters
    adults, children, infants = 1, 0, 0
    class_type, referer = 'E', 'home'

    # origin_code, origin_name, dest_code, dest_name, 
    #                            adults, children, infants, class_type, 
    #                            departure_date, referer='home'

    # Generate URL for scraping
    url = generate_paytm_flight_url(
        origin_code, origin_name, dest_code, dest_name,
        adults, children, infants, class_type, departure_date,  referer
    )

    driver = webdriver.Chrome()

    print(f"url ____>>>> {url}" )
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

                # flights_data.append({
                #     'airline': airline,
                #     # 'airline_logo': airline_logo,
                #     'departure_time': departure_time,
                #     'arrival_time': arrival_time,
                #     'duration': duration_text,
                #     'final_price': int(price),
                #     # 'fare_type': fare_type,
                #     # 'offer': offer,
                #     'layover': str(layover),
                #     'url': get_booking_url(driver, flight_id)
                # })


                flights_data.append({
                    # 'flight_id': flight_id,
                    'airline': airline,
                    'airline_logo': airline_logo,
                    'departure_time': departure_time,
                    'departure_city': departure_city,
                    'arrival_time': arrival_time,
                    'arrival_city': arrival_city,
                    'duration': duration_text.split()[1] + ' ' + duration_text.split()[2],
                    'price':  str(int(price)),
                    'fare_type': fare_type,
                    'offer': offer,
                    'layover': str(layover),
                    'url' : get_booking_url(driver, flight_id)
                })

                if len(flights_data) >= 5:  # Limit to 5 flights
                    break

            except Exception:
                continue

        driver.quit()

        return {
            "type": "airplane",
            "data": flights_data
        }

    except Exception as e:
        driver.quit()
        return {"error": str(e)}



if __name__ == "__main__":

    driver = scrape_flights( "Delhi", "Jaipur", departure_date="2025-02-23")
    print(driver)
