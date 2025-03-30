"""
XPath Selectors for Paytm Bus Scraping

This module contains XPath selectors used for scraping bus information from Paytm's bus booking platform.
These selectors are used to locate and extract specific elements from the Paytm bus search results page.

Note:
    These XPath selectors are specific to Paytm's current HTML structure and may need to be updated
    if the website's structure changes.

Variables:
    cards_xpath (str): XPath to locate the container of all bus cards
    bus_name_xpath (str): XPath to locate the bus operator name within a card
    bus_type_xpath (str): XPath to locate the bus type/class within a card
    departure_time_xpath (str): XPath to locate the departure time within a card
    departure_date_xpath (str): XPath to locate the departure date within a card
    arrival_time_xpath (str): XPath to locate the arrival time within a card
    arrival_date_xpath (str): XPath to locate the arrival date within a card
    duration_xpath (str): XPath to locate the journey duration within a card
    final_price_xpath (str): XPath to locate the final price within a card
    rating_xpath (str): XPath to locate the bus rating within a card
    seats_available_xpath (str): XPath to locate the number of available seats within a card
"""

# Main container for all bus cards
cards_xpath = "//div[@class='IHKeM']" 

# Bus information selectors (relative to each card)
bus_name_xpath = "//div[@class='+iUf5']"  # Bus operator name
bus_type_xpath = "//div[@class='G88l9']"  # Bus type/class

# Departure information selectors
departure_time_xpath = "//div[@class='wYtCy']//div[@class='_4rWgi']"  # Departure time
departure_date_xpath = "//div[@class='wYtCy']//div[@class='C3vrs']"   # Departure date

# Arrival information selectors
arrival_time_xpath = "//div[@class='EjC2U']//div[@class='_4rWgi']"    # Arrival time
arrival_date_xpath = "//div[@class='EjC2U']//div[@class='C3vrs']"     # Arrival date

# Additional information selectors
duration_xpath = "//div[@class='_1D2hF']"           # Journey duration
final_price_xpath = "//span[@class='A2eT9 F+C81']"  # Final price
rating_xpath = "//div[@class='eoyaT']/div"          # Bus rating
seats_available_xpath = "//div[@class='UxGbP'][1]"  # Available seats
