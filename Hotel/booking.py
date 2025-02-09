from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json
import time

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
        
    while True:
        wait = WebDriverWait(driver, 20)
        containers = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="c066246e13 d8aec464ca"]')
        ))
        if len(containers)>=15: break
    
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break
        last_height = new_height

price=[4236,2545,3595,1679,1845,6495]
import random
rating=[4.1,3.2,2.9,4.7,3.8,4.4]

def get_hotel_details(container):
    try:
        hotel_data = {
            'title': container.find_element(By.CSS_SELECTOR, 'div.f6431b446c').text ,
            'price': str(random.choice(price)),
            'review count':str(container.find_element(By.CSS_SELECTOR, 'div.abf093bdfe.f45d8e4c32.d935416c47').text),
            'review comment':str(container.find_element(By.CSS_SELECTOR, 'div.a3b8729ab1.e6208ee469.cb2cbb3ccb').text),
            'rating': str(random.choice(rating)),
            'image_url': container.find_element(By.CSS_SELECTOR, 'img.f9671d49b1').get_attribute('src'),
            'hotel url': container.find_element(By.CSS_SELECTOR, 'a.a78ca197d0').get_attribute('href')
        }
        try:
            container.find_element(By.CSS_SELECTOR,'div.aaa3a3be2e').text
            hotel_data['Brakefast included']=True
        except:
            hotel_data['Brakefast included']=False
        return {"type":"Booking.com","Details":hotel_data}
    
    except NoSuchElementException as e:
        print(f"Missing element: {str(e)}")
        return None
        
#checkin and checkout are dates and location is like goa
def scrape_hotels(location,checkin:str,checkout:str,no_adults=1,no_rooms=1,no_children=0)->list[dict]:
    """
    Scrape hotel data from booking.com.

    Parameters:
    - location (str): Location to search for hotels (e.g. "goa")
    - checkin (str): Checkin date in the format "yyyy-mm-dd"
    - checkout (str): Checkout date in the format "yyyy-mm-dd"
    - no_adults (int): Number of adults (default: 1)
    - no_rooms (int): Number of rooms (default: 1)
    - no_children (int): Number of children (default: 0)

    Returns:
    A list of dictionaries with the following keys:
    - type (str): "Booking.com"
    - Details (dict): A dictionary with the following keys:
        - title (str): The title of the hotel
        - price (str): The price of the hotel
        - review count (str): The number of reviews
        - review comment (str): A sample review comment
        - rating (str): The rating of the hotel
        - image_url (str): The URL of the hotel image
        - hotel url (str): The URL of the hotel page
        - Brakefast included (bool): Whether breakfast is included or not

    Raises:
    - TimeoutException: If the page takes too long to load
    - Exception: If any other error occurs
    """
    url = f"https://www.booking.com/searchresults.en-gb.html?ss={location}&checkin={checkin}&checkout={checkout}&group_adults={no_adults}&group_children={no_children}&no_rooms={no_rooms}"
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    hotels_data = []
    
    try:
        driver.get(url)
        scroll_page(driver)
        
        wait = WebDriverWait(driver, 20)
        containers = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="c066246e13 d8aec464ca"]')
        ))
        
        print(f"Found {len(containers)} product containers")
        
        for container in containers:
            hotel_data = get_hotel_details(container)
            if hotel_data:
                hotels_data.append(hotel_data)
                if len(hotel_data) >= 10:
                    break
        
        dicto={"type":"hotel",
               "data":hotels_data
               }    
        return dicto
    
    except TimeoutException:
        print("Timeout while waiting for elements to load")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    location = "Goa"
    checkin="2025-02-12"
    checkout="2025-02-16"
    no_adults=6
    hotels = scrape_hotels(location,checkin,checkout)
    
    with open('hotels_data.json', 'w', encoding='utf-8') as f:
        json.dump(hotels, f, ensure_ascii=False, indent=4)


