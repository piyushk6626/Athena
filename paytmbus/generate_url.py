# URL: tickets.paytm.com.com/bus/search/{SOURCE}/{DESTINATION}/{JOURNEY-DATE}/1?URL
# DATE_FORMAT: YYYY-MM-DD
# SOURCE: First letter of city is capital
# DESTINATION: First letter of city is capital
import web_scrape 
def generate_paytm_bus_url(source, destination, journey_date):
    """
    Generate a Paytm Bus URL and return the scraped data.

    Args:
        source (str): Source city name. The first letter of the city name is capitalized.
        destination (str): Destination city name. The first letter of the city name is capitalized.
        journey_date (str): Date of journey in the format YYYY-MM-DD.

    Returns:
        dict: A dictionary containing the scraped data.

    Raises:
        ValueError: If the date format is invalid.
    """
    from datetime import datetime
    
    try:
        datetime.strptime(journey_date, "%Y-%m-%d")
        
        source = source.capitalize()
        destination = destination.capitalize()
        
        url = f"https://tickets.paytm.com/bus/search/{source}/{destination}/{journey_date}/1"
        return web_scrape.get_bus_data(url)
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

if __name__ == "__main__":
    source = "Bangalore"
    destination = "Pune"
    journey_date = "2025-03-01"
    
    url = generate_paytm_bus_url(source, destination, journey_date)
    print(web_scrape.get_bus_data(url))