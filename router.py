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
from Spotify import process_input
from Paytmflights import script
# print(sonar.serach_the_web_for_news("What is the weather in Goa?"))  # working
 
# print(uber_link.automate_uber_ride("Empire State", "Central Park")) # working but needs login

# print(airbnb_func.scrape_airbnb("goa", "2025-02-09", "2025-02-14", "1", "0")) # working

# print(scrapping.scrape_products_from_amazon("laptop")) #working

# print(email_automation.send_email('siddhantganesh25@gmail.com', 'Generated Email', 'Hello 1234')) #working

# print(carter.fashion_search_api("Clothes for wedding")) #working


# def scrape_hotels(location,checkin:str,checkout:str,no_adults=1,no_rooms=1,no_children=0)->list[dict]:
# print(booking.scrape_hotels("goa","2025-02-09","2025-02-14")) #working 



# # Example: Scrape movies in a city.
# movies_json = scrape_movies("pune")
# print(movies_json)

# #Example: Extract show details.
# shows = extract_movie_shows("https://paytm.com/movies/interstellar-2014-movie-detail-288?frmtid=zrwlluqk8", "pune", "english")
# print(shows)

# print(restaurant_search.find_similar_items("Fast food near me")) # working

# def callfunction(name, args):
#     response = None
#     if name == "serach_the_web_for_news":
#         response = sonar.serach_the_web_for_news(**args)
#     elif name == "automate_uber_ride":
#         response = uber_link.automate_uber_ride(**args)
#     elif name == "scrape_airbnb":
#         response = airbnb_func.scrape_airbnb(**args)
#     elif name == "find_similar_restaurants":
#         response = restaurant_search.find_similar_items(**args)
#     elif name == "scrape_movies":
#         response = scrape_movies(**args)
#     elif name == "extract_single_movie_show" :
#         response = extract_movie_shows(**args)
#     elif name == "find_hotels":
#         response = booking.scrape_hotels(**args)
#     elif name == "find_products_from_amazon":
#         response = scrapping.scrape_products_from_amazon(**args)
#     elif name == "fashion_search_api":
#         response = carter.fashion_search_api(**args)
#     elif name == "send_email_tool":
#         response = email_automation.send_email(**args)
#     elif name == "get_bus_data":
#         response = generate_url.generate_paytm_bus_url(**args)
#     elif name == "Spotify_action_bot":
#         response == process_input.process_input(**args)
#     return response


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
        case "Spotify_action_bot":
            response == process_input.process_input(**args)
        case "scrape_flights":
            response = script.scrape_flights(**args)
        case _:
            response = None
    return response 

            
        
        












