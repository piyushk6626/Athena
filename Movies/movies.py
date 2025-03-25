# paytm_scraper/movies.py

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .utils import scroll_page, input_city_and_select_first, select_language
from .xpath import (
    MOVIE_CARD, MOVIE_POSTER, MOVIE_LINK, MOVIE_TITLE,
    MOVIE_AGE_RATING, MOVIE_LANGUAGE, VIEW_MORE_BUTTON,
    OVERLAY_BACKDROP, THEATER_SESSIONS, THEATER_NAME,
    SHOW_TIMES, TIME_SLOT, MOVIE_FORMAT
)

def scrape_movies(city):
    """
    Scrapes the list of movies available in the given city.
    Returns a JSON string with movie details.
    """
    # Construct the URL for the given city
    url = f"https://paytm.com/movies/{city}"

    # Set up Chrome options and initialize driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Allow the page to load

    # Try clicking the 'View More' button if available
    try:
        # Click the overlay backdrop first
        button = driver.find_element(By.XPATH, OVERLAY_BACKDROP)
        driver.execute_script("arguments[0].click();", button)
        
        # Wait for and click the 'View More' button
        view_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, VIEW_MORE_BUTTON))
        )
        driver.execute_script("arguments[0].scrollIntoView();", view_more_button)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, -200);")  # Scroll up slightly for better visibility
        time.sleep(1)
        driver.execute_script("arguments[0].click();", view_more_button)
        time.sleep(3)
    except (NoSuchElementException, TimeoutException):
        print("No 'View More' button found or clickable.")

    # Extract movie details
    movies = []
    movie_elements = driver.find_elements(By.XPATH, MOVIE_CARD)
    
    # Process each movie card
    for movie in movie_elements:
        try:
            # Extract all required information from the movie card
            poster = movie.find_element(By.XPATH, MOVIE_POSTER).get_attribute("src")
            link = movie.find_element(By.XPATH, MOVIE_LINK).get_attribute("href")
            title = movie.find_element(By.XPATH, MOVIE_TITLE).text
            age_rating = movie.find_element(By.XPATH, MOVIE_AGE_RATING).text
            language = movie.find_element(By.XPATH, MOVIE_LANGUAGE).text

            # Add movie details to the list
            movies.append({
                "title": title,
                "poster": poster,
                "link": link,
                "age_rating": age_rating,
                "language": language
            })

            # Limit to 10 movies
            if len(movies) == 10:
                break
        except NoSuchElementException:
            continue

    # Clean up and return results
    driver.quit()
    dicto = {
        "type": "moviesList",
        "data": json.dumps(movies)
    }
    return dicto

def _extract_movie_shows(driver):
    """
    Helper function that extracts movie show details from the page.
    Returns a list of dictionaries containing show information.
    """
    movie_data = []
    try:
        # Get all theater sessions
        theaters = driver.find_elements(By.XPATH, THEATER_SESSIONS)
        
        # Process each theater
        for theater in theaters:
            try:
                # Get theater name
                name = theater.find_element(By.XPATH, THEATER_NAME).text
                showtimes = []
                
                # Get all show times for this theater
                show_elements = theater.find_elements(By.XPATH, SHOW_TIMES)
                
                # Process each show time
                for show in show_elements:
                    try:
                        # Extract time slot information
                        time_slot_text = show.find_element(By.XPATH, TIME_SLOT).text
                        parts = time_slot_text.split("\n")
                        time_value = parts[0]
                        special = parts[1] if len(parts) > 1 else "N/A"
                        
                        # Try to get movie format (2D, 3D, etc.)
                        try:
                            movie_format = show.find_element(By.XPATH, MOVIE_FORMAT).text
                        except Exception:
                            movie_format = "2D"
                            
                        # Create show time entry
                        show_entry = {
                            "time": time_value,
                            "special": special,
                            "format": movie_format,
                            "theater": name,
                            "url": driver.current_url
                        }
                        
                        # Add to both lists
                        showtimes.append(show_entry)
                        movie_data.append(show_entry)
                        
                    except Exception:
                        continue

            except Exception:
                continue
    except Exception:
        print("Failed to extract movie show details.")

    return movie_data

def extract_movie_shows(url, city, language):
    """
    Extracts movie show details from the Paytm page after selecting the specified city and language.
    Returns a list of dictionaries containing the show details.
    """
    # Set up Chrome options and initialize driver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to the page and set up city and language
        input_city_and_select_first(driver, city, url)
        select_language(driver, language)
        scroll_page(driver)
        
        # Extract show details
        shows = _extract_movie_shows(driver)
    finally:
        driver.quit()
    
    # Format and return results
    dicto = {
        "type": "moviesTiming",
        "data": shows
    }
    return dicto

if __name__ == "__main__":
    # Test the functionality
    data = extract_movie_shows("https://paytm.com/movies", "Pune", "English")
    print(json.dumps(data, indent=2))