"""
Paytm Movie Booking Scraper

This package provides functionality to scrape and interact with Paytm's movie booking platform.
It includes modules for scraping movie listings, show timings, seat layouts, and handling the booking process.

Modules:
    movies.py: Contains functions for scraping movie listings and show timings
    seats.py: Handles seat layout scraping and booking functionality
    utils.py: Contains utility functions for common operations
    xpath.py: Contains all XPath constants used across the package

Classes:
    SeatScraper: Scrapes seat information from a given URL
    SeatBooking: Handles the seat selection and booking process

Functions:
    scrape_movies(city): Scrapes the list of movies available in the given city
    extract_movie_shows(url, city, language): Extracts movie show details for a specific movie
    extract_seat_details(url, city, language, theater_name, show_time): Gets seat layout details
    select_given_seat_and_click_book_ticket(url, seat_rows, seat_numbers): Handles seat selection and booking

Dependencies:
    - selenium: For web automation
    - beautifulsoup4: For HTML parsing
    - time: For handling delays and waits

Usage Example:
    from Movies import scrape_movies, extract_movie_shows, extract_seat_details

    # Get list of movies in a city
    movies = scrape_movies("Mumbai")

    # Get show timings for a specific movie
    shows = extract_movie_shows("https://paytm.com/movies", "Mumbai", "English")

    # Get seat details for a specific show
    url, seats = extract_seat_details(
        "https://paytm.com/movies",
        "Mumbai",
        "English",
        "PVR Cinemas",
        "2:30 PM"
    )

Note:
    This package requires Chrome browser and ChromeDriver to be installed.
    Make sure to handle the webdriver setup appropriately in your environment.
"""

from .movies import scrape_movies, extract_movie_shows
from .seats import extract_seat_details, select_given_seat_and_click_book_ticket
from .utils import scroll_page, input_city_and_select_first, select_language, click_button_and_get_url

__all__ = [
    'scrape_movies',
    'extract_movie_shows',
    'extract_seat_details',
    'select_given_seat_and_click_book_ticket',
    'scroll_page',
    'input_city_and_select_first',
    'select_language',
    'click_button_and_get_url'
]
