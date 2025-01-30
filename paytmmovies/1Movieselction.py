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

def scrape_movies():
    url = "https://paytm.com/movies/pune"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    try:
        # Click 'View More' button if available
        view_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='ViewMore_viewAll__KJ5c1']/span"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", view_more_button)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, -200);")  # Move up slightly before clicking
        time.sleep(1)
        driver.execute_script("arguments[0].click();", view_more_button)

        time.sleep(3)  # Wait for new content to load
    except (NoSuchElementException, TimeoutException):
        print("No 'View More' button found or clickable.")

    # Scroll to the bottom to load all movies
    scroll_page(driver)

    # Scrape movie details
    movies = []
    movie_elements = driver.find_elements(By.XPATH, "//div[@class='DesktopRunningMovie_movieCard__p5n6P']")
    
    for movie in movie_elements:
        try:
            poster = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_imgCon__XM_UA']/img").get_attribute("src")
            link = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_runningMovie__N17Hp']/a").get_attribute("href")
            title = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_movTitle__Q1pOY']").text
            age_rating = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_point__YtD_w']/span").text
            language = movie.find_element(By.XPATH, ".//div[@class='DesktopRunningMovie_point__YtD_w']/span[@class='textClamp']").text
            
            movies.append({
                "title": title,
                "poster": poster,
                "link": link,
                "age_rating": age_rating,
                "language": language
            })
        except NoSuchElementException:
            continue
    
    driver.quit()
    return json.dumps(movies, indent=4)

if __name__ == "__main__":
    movie_data = scrape_movies()
    print(movie_data)
