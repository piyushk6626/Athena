from webserch import sonar
from uber import uber_link
from airbnb import airbnb_func
from Amazon import scrapping 
from emailAutomation import email_automation  
from FashionShopping import carter
from Hotel import booking

# print(sonar.serach_the_web_for_news("What is the weather in Goa?"))  # working
 
# print(uber_link.automate_uber_ride("Empire State", "Central Park")) # working but needs login

# print(airbnb_func.scrape_airbnb("goa", "2025-02-09", "2025-02-14", "1", "0")) # working

print(scrapping.scrape_products_from_amazon("laptop")) #working

# print(email_automation.send_email('siddhantganesh25@gmail.com', 'Generated Email', 'Hello 1234')) #working

# print(carter.call_fashion_search_api("Clothes for wedding")) #working


# def scrape_hotels(location,checkin:str,checkout:str,no_adults=1,no_rooms=1,no_children=0)->list[dict]:
# print(booking.scrape_hotels("goa","2025-02-09","2025-02-14")) #working but returns only one hotel














