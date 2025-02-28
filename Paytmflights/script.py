# https://www.in.cheapflights.com/flight-search/BOM-BLR/2025-03-11?ucs=12mksjb


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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


def scrape_flights(origin_name, dest_name, departure_date):
    url = f"https://www.in.cheapflights.com/flight-search/{INDIAN_AIRPORT_CODES[origin_name]}-{INDIAN_AIRPORT_CODES[dest_name]}/{departure_date}?ucs=12mksjb"
    print(url)

    return scrape_flights_from_url(url,origin_name,dest_name)
    



def scrape_flights_from_url(url, origin, destination):
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    driver.get(url)
    time.sleep(2)
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
    results = scrape_flights("Bangalore", "Mumbai", "2025-03-03")
    
    print(results)

# CHEAPFLIGHTS.COM
# PARENT //div[@class="Fxw9-result-item-container"]/div[@class="nrc6 nrc6-mod-pres-default nrc6-mod-desktop-responsive"]
# URL //a[@role="link" and @class="Iqt3 Iqt3-mod-stretch Iqt3-mod-bold Button-No-Standard-Style Iqt3-mod-variant-solid Iqt3-mod-theme-progress-legacy Iqt3-mod-shape-rounded-small Iqt3-mod-shape-mod-default Iqt3-mod-spacing-default Iqt3-mod-size-small"]
# PRICE //div[@class="f8F1-price-text-container"]/div[@class="f8F1-price-text"]
# DEPARTURE (//div[@class="vmXl vmXl-mod-variant-large"]/span)[1]
# ARRIVAL (//div[@class="vmXl vmXl-mod-variant-large"]/span)[3]
# DURATION //div[@class="xdW8 xdW8-mod-full-airport"]/div[@class="vmXl vmXl-mod-variant-default"]
# STOPS //span[@class="JWEO-stops-text"]
# IMAGE //img src of this element
# FLIGHT NAME  //img ALT of this element
