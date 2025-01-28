#MovieSlectionElement = //a[@class="sc-133848s-11 sc-1ljcxl3-1 cxWSPX"] and it must contain //div[@class="sc-dv5ht7-0 XmXCP"]
# INSIDE THIS DIV FOLLOWING XPath
#   PhotoElement =  //div[@class="sc-133848s-2 sc-1t5vwh0-1 gTzZQd"]
#   MovieNameElement = //div[@class="sc-7o7nez-0 hGuczM"]
#   Movie Age Rating Element = (//div[@class="sc-7o7nez-0 ifFqly"])[1]
#   Movie Language Element = (//div[@class="sc-7o7nez-0 ifFqly"])[2]

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json

def scroll_page(driver):
    """Scroll the page by 1000px increments to load dynamic JavaScript content"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    
    while True:
        # Scroll down by 1000 pixels
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2)  # Adjust sleep time based on page loading speed
        
        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break
        
        last_height = new_height

def get_movie_details(movie_element):
    """Extract details from a single movie card element"""
    try:
        # Find the container div that holds all movie details
        container = movie_element.find_element(By.XPATH, './/div[@class="sc-dv5ht7-0 XmXCP"]')
        
        # Locate the div that contains the image
        photo_div = container.find_element(
            By.XPATH, './/div[@class="sc-133848s-2 sc-1t5vwh0-1 gTzZQd"]'
        )
        
        # Within this div, find the img element
        img_element = photo_div.find_element(By.TAG_NAME, 'img')
        
        # Extract the src and alt attributes from the img
        photo_url = img_element.get_attribute('src')
        movie_name_alt = img_element.get_attribute('alt')
        
        # Extract the movie name from the designated element
        movie_name_element = container.find_element(
            By.XPATH, './/div[@class="sc-7o7nez-0 hGuczM"]'
        ).text
        
        # Extract age ratings and language
        age_rating_elements = container.find_elements(
            By.XPATH, './/div[@class="sc-7o7nez-0 ifFqly"]'
        )
        
        age_rating = age_rating_elements[0].text if len(age_rating_elements) > 0 else "N/A"
        language = age_rating_elements[1].text if len(age_rating_elements) > 1 else "N/A"
        
        return {
            'movie_name_alt': movie_name_alt,  # From img alt attribute
            'movie_name': movie_name_element,   # From designated text element
            'photo_url': photo_url,
            'age_rating': age_rating,
            'language': language,
            'movie_url': movie_element.get_attribute('href')
        }
    except (NoSuchElementException, IndexError) as e:
        print(f"Error extracting movie details: {str(e)}")
        return None

def scrape_movies(url):
    """Main function to scrape all movie cards from the page"""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is in PATH
    movies_data = []
    
    try:
        # Load the page
        driver.get(url)
        
        # Scroll to load all dynamic content
        scroll_page(driver)
        
        # Wait for movie cards to be present
        wait = WebDriverWait(driver, 20)
        movie_elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//a[contains(@class, "sc-133848s-11") and contains(@class, "cxWSPX")]')
        ))
        print(f"Found {len(movie_elements)} movie elements.")
        
        # Extract data from each movie card
        for index, movie_element in enumerate(movie_elements, start=1):
            movie_data = get_movie_details(movie_element)
            if movie_data:
                movies_data.append(movie_data)
            else:
                print(f"Skipping movie at index {index} due to extraction error.")
        
        return movies_data
    
    except TimeoutException:
        print("Timeout while waiting for elements to load")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    finally:
        driver.quit()
        
# Example usage
if __name__ == "__main__":
    # Replace with your target URL
    target_url = "https://in.bookmyshow.com/explore/movies-pune"
    movies = scrape_movies(target_url)
    
    # Save results to a JSON file
    with open('movies_data.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)
    
    # Optionally, print a summary
    print(f"Scraped {len(movies)} movies.")
