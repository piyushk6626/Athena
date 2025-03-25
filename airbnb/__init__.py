"""
Airbnb Scraper Package
======================

A comprehensive web scraping solution for extracting Airbnb listing information using Selenium WebDriver.

Package Overview
--------------
This package provides a robust set of tools for automated scraping of Airbnb listings,
including property details, pricing, and availability information. It handles web automation,
data extraction, and text cleaning in a modular and maintainable way.

Key Components
------------
1. AirbnbScraper: Main scraper class that orchestrates the entire scraping process
   - Manages WebDriver lifecycle
   - Handles URL construction
   - Extracts listing information
   - Processes multiple listings concurrently

2. TextCleaner: Utility class for sanitizing and formatting scraped text
   - Removes unwanted characters
   - Standardizes formatting
   - Handles price cleaning
   - Sanitizes special characters

3. WebDriverManager: Handles Chrome WebDriver setup and configuration
   - Manages driver initialization
   - Handles driver cleanup
   - Configures browser options

Main Features
-----------
- Automated listing data extraction
- Configurable search parameters (location, dates, guests)
- Robust error handling and recovery
- Clean text processing
- Structured data output
- Memory-efficient processing

Usage Example
-----------
>>> from airbnb import scrape_airbnb
>>> 
>>> # Configure search parameters
>>> results = scrape_airbnb(
...     destination="New York",
...     checkin_date="2024-06-01",
...     checkout_date="2024-06-07",
...     adults_no="2",
...     children_no="0"
... )
>>> 
>>> # Access the scraped data
>>> for listing in results['data']:
...     print(f"Property: {listing['hotel_name']}")
...     print(f"Price: {listing['total_price']}")
...     print(f"Location: {listing['location']}")

Return Data Structure
------------------
{
    'type': 'airbnb',
    'data': [
        {
            'image_url': str,      # URL of the property image
            'hotel_name': str,     # Name/title of the property
            'payment_url': str,    # Direct booking URL
            'location': str,       # Property location
            'total_price': str,    # Price per night (without currency symbol)
            'rating_reviews': str, # Rating and review information
            'tag_text': str       # Property tags/features
        },
        ...
    ]
}

Dependencies
-----------
- selenium: Web automation and scraping
- re: Regular expression operations
- json: Data serialization
- time: Timing and delays

Requirements
-----------
- Python 3.7+
- Chrome WebDriver
- Google Chrome Browser
- Selenium 4.0+

Notes
-----
1. Respect Airbnb's robots.txt and terms of service
2. Implement appropriate delays between requests
3. Handle rate limiting and IP blocking scenarios
4. Keep WebDriver and Chrome browser updated
5. Consider using proxy rotation for large-scale scraping


"""

from .airbnb_func import (
    AirbnbScraper,
    TextCleaner,
    WebDriverManager,
    scrape_airbnb
)

from .xpath import (
    imgpath,
    hotelnamepath,
    paymentpath,
    locationpath,
    totalpricepath,
    ratingreviews,
    tagpath
)

__version__ = '1.0.0'
__author__ = 'Your Name'
__license__ = 'MIT'

__all__ = [
    'AirbnbScraper',
    'TextCleaner',
    'WebDriverManager',
    'scrape_airbnb',
    'imgpath',
    'hotelnamepath',
    'paymentpath',
    'locationpath',
    'totalpricepath',
    'ratingreviews',
    'tagpath'
]