# paytm_scraper/movies.py

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from .utils import scroll_page, input_city_and_select_first, select_language
from .utils import scroll_page, input_city_and_select_first, select_language


def scrape_movies(city):
    """
    Scrapes the list of movies available in the given city.
    Returns a JSON string with movie details.
    """
    url = f"https://paytm.com/movies/{city}"

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Allow the page to load

    # Try clicking the 'View More' button if available
    try:
        button = driver.find_element(By.XPATH, "//div[@class='Overlay_backdrop__F12DQ']")
        driver.execute_script("arguments[0].click();",button)
        
        view_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='ViewMore_viewAll__KJ5c1']/span")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView();", view_more_button)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, -200);")
        time.sleep(1)
        driver.execute_script("arguments[0].click();", view_more_button)
        time.sleep(3)
    except (NoSuchElementException, TimeoutException):
        print("No 'View More' button found or clickable.")

    # Scroll down to load all content

    # Extract movie details
    movies = []
    movie_elements = driver.find_elements(
        By.XPATH, "//div[@class='DesktopRunningMovie_movieCard__p5n6P']"
    )
    for movie in movie_elements:
        try:
            poster = movie.find_element(
                By.XPATH, ".//div[@class='DesktopRunningMovie_imgCon__XM_UA']/img"
            ).get_attribute("src")
            link = movie.find_element(
                By.XPATH, ".//div[@class='DesktopRunningMovie_runningMovie__N17Hp']/a"
            ).get_attribute("href")
            title = movie.find_element(
                By.XPATH, ".//div[@class='DesktopRunningMovie_movTitle__Q1pOY']"
            ).text
            age_rating = movie.find_element(
                By.XPATH, ".//div[@class='DesktopRunningMovie_point__YtD_w']/span"
            ).text
            language = movie.find_element(
                By.XPATH, ".//div[@class='DesktopRunningMovie_point__YtD_w']/span[@class='textClamp']"
            ).text

            movies.append({
                "title": title,
                "poster": poster,
                "link": link,
                "age_rating": age_rating,
                "language": language
            })

            if len(movies) == 10:
                break
        except NoSuchElementException:
            continue

    driver.quit()
    dicto={
        "type" : "moviesList",
        "data" : json.dumps(movies)
    }
    return dicto

def _extract_movie_shows(driver):
    """
    Helper function that extracts movie show details from the page.
    """
    movie_data = []
    try:
        theaters = driver.find_elements(
            By.XPATH, "//div[@class='MovieSessionsListingDesktop_movieSessions__KYv1d']"
        )
        for theater in theaters:
            try:
                name = theater.find_element(
                    By.XPATH, ".//div[@class='MovieSessionsListingDesktop_details__Aq3st']/a"
                ).text
                showtimes = []
                show_elements = theater.find_elements(
                    By.XPATH, ".//div[contains(@class, 'MovieSessionsListingDesktop_timeblock__MiYNc')]"
                )
                for show in show_elements:
                    try:
                        time_slot_text = show.find_element(
                            By.XPATH, ".//div[contains(@class, 'MovieSessionsListingDesktop_time__r6FAI')]"
                        ).text
                        parts = time_slot_text.split("\n")
                        time_value = parts[0]
                        special = parts[1] if len(parts) > 1 else "N/A"
                        try:
                            movie_format = show.find_element(
                                By.XPATH, ".//div[@class='MovieSessionsListingDesktop_premiumLabel__ed70A']"
                            ).text
                        except Exception:
                            movie_format = "2D"
                        showtimes.append({
                            "time": time_value,
                            "special": special,
                            "format": movie_format,
                            "theater": name,
                            "url": driver.current_url
                        })

                        movie_data.append({
                            "time": time_value,
                            "special": special,
                            "format": movie_format,
                            "theater": name,
                            "url": driver.current_url
                        })
                    except Exception:
                        continue

                # movie_data.append(showtimes)


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
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    try:
        input_city_and_select_first(driver, city, url)
        select_language(driver, language)
        scroll_page(driver)
        shows = _extract_movie_shows(driver)
    finally:
        driver.quit()
    
    dicto={
        "type":"moviesTiming",
        "data": shows
    }
    return dicto


if __name__ == "__main__":
    data = extract_movie_shows("https://paytm.com/movies", "Pune", "English")
    print(json.dumps(data, indent=2))