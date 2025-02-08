from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs, unquote
import json
import time

def fill_location_input(driver, input_xpath, location):
    try:
        # Wait for input field to be present
        input_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, input_xpath))
        )
       
        # Scroll to element
        driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
       
        # Click to focus the input
        input_element.click()
        time.sleep(0.5)
       
        # Create action chains for keyboard input
        actions = ActionChains(driver)
        
        # Type each character directly via keyboard
        for char in location:
            actions.send_keys(char)
            actions.pause(0.1)  # Small delay between characters
        
        # Perform the accumulated actions
        actions.perform()
       
        # Wait for autocomplete suggestions
        time.sleep(1)
       
        # Use keyboard to select first suggestion
        actions = ActionChains(driver)
        actions.send_keys(Keys.DOWN)
        actions.pause(0.5)
        actions.send_keys(Keys.ENTER)
        actions.perform()
       
        print(f"Successfully entered location: {location}")
        return input_element
   
    except Exception as e:
        print(f"Error filling location input: {str(e)}")
        raise e
    

def automate_uber_ride(pickup_location, destination):
    # Set up Chrome options
    """
    Automates the process of booking an Uber ride using a web browser.

    This function uses Selenium WebDriver to interact with the Uber mobile site. It sets up Chrome browser options,
    navigates to the Uber site, fills in the pickup and destination locations, and clicks the "See Prices" button.

    Args:
        pickup_location (str): The address or name of the pickup location.
        destination (str): The address or name of the destination.

    Returns:
        dict: A dictionary containing the URL to view ride .

    Raises:
        Exception: If an error occurs during the process, an exception is raised and a screenshot is saved.
    """

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to Uber mobile site
        
        driver.get("https://m.uber.com/go/pickup?effect=")

        a = 30

        while(a):
            a = a - 1
            time.sleep(1)
            print(a)

        
        # Wait for page to load completely
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@aria-autocomplete='list'])[1]"))
        )
        
        # Fill pickup location (first input)
        xpathforlocation =  "(//input)[1]"
        fill_location_input(driver, xpathforlocation, pickup_location)
        
        # Wait briefly between inputs
        time.sleep(1)
        
        # Fill destination (second input)

        xpathfordest =  "(//input)[2]"
        fill_location_input(driver, xpathfordest, destination)
        
        # Wait for "See Prices" button to be clickable
        see_prices_xpath = "//button[@class = '_css-hUNeqW']"
        see_prices_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, see_prices_xpath))
        )
        
        # Scroll to and click "See Prices" button
        driver.execute_script("arguments[0].scrollIntoView(true);", see_prices_button)
        see_prices_button.click()
        
        print("Clicked 'See Prices' button")
        current_url = driver.current_url


        # return {"type":"Uber","data":{"see prices url":current_url}}
        print(f"url {current_url}")
        return extract_uber_locations(current_url)
        # Keep browser open to view results
        #time.sleep(300)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
        raise e
    finally:
        #time.sleep(300)
        driver.quit()


def extract_uber_locations(url):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    
    # Safely extract pickup and drop-off parameters
    pickup_json = params.get('pickup', [None])[0]
    drop_json = params.get('drop[0]', [None])[0]  # Use decoded key 'drop[0]'
    
    if not pickup_json or not drop_json:
        raise ValueError("Missing pickup/drop parameters in the URL")
    
    # Parse JSON data
    pickup_data = json.loads(unquote(pickup_json))
    drop_data = json.loads(unquote(drop_json))
    
    return {
        'type': 'Uber',
        'url': url,
        'pickup': {
            'name': pickup_data['addressLine1'],
            'address': pickup_data['addressLine2'],
            'latitude': pickup_data['latitude'],
            'longitude': pickup_data['longitude']
        },
        'dropoff': {
            'name': drop_data['addressLine1'],
            'address': drop_data['addressLine2'],
            'latitude': drop_data['latitude'],
            'longitude': drop_data['longitude']
        }
    }

if __name__ == "__main__":
    main_data=[]
    try:
        data = automate_uber_ride("Siddhi Vinayak", "Marine drive")
        print(data)
        main_data.append(data)
    except Exception as e:
        print(f"Script failed: {str(e)}")
    with open('rides_data.json', 'w', encoding='utf-8') as f:
        json.dump(main_data, f, ensure_ascii=False, indent=4)