from webserch import sonar
from uber import uber_link
from airbnb import airbnb_func
from Amazon import scrapping 
from emailAutomation import email_automation  
from FashionShopping import carter
from Hotel import booking
from Movies import (
    scrape_movies,
    extract_movie_shows,
    extract_seat_details,
    select_given_seat_and_click_book_ticket,
)
from restaurant import search as restaurant_search
from paytmbus import generate_url
from Paytmflights import script
from zepto.order import scrape_zepto
from emailAutomation.email_automation import read_emails, send_email
from Spotify.function import *


def callfunction(name, args):
    response = None
    match name:
        case "serach_the_web_for_news":
            response = sonar.serach_the_web_for_news(**args)
        case "automate_uber_ride":
            response = uber_link.automate_uber_ride(**args)
        case "scrape_airbnb":
            response = airbnb_func.scrape_airbnb(**args)
        case "find_similar_restaurants":
            response = restaurant_search.find_similar_items(**args)
        case "scrape_movies":
            response = scrape_movies(**args)
        case "extract_single_movie_show" :
            response = extract_movie_shows(**args)
        case "find_hotels":
            response = booking.scrape_hotels(**args)
        case "find_products_from_amazon":
            response = scrapping.scrape_products_from_amazon(**args)
        case "fashion_search_api":
            response = carter.fashion_search_api(**args)
        case "send_email_tool":
            response = email_automation.send_email(**args)
        case "get_bus_data":
            response = generate_url.generate_paytm_bus_url(**args)
        case "play_song":
            response = play_song(**args)
        case "pause_playback":
            response = pause_playback(**args)        
        case "scrape_flights":
            response = script.scrape_flights(**args)
        case "scrape_zepto":
            response = scrape_zepto(**args)
        case "send_email":
            response = send_email(**args)
        case _:
            response = None
    return response 

            
        
        












