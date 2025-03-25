"""
Paytm Bus Booking Module

This package provides functionality to interact with Paytm's bus booking platform,
allowing users to search for bus routes, get pricing information, and check availability.

The package uses Selenium WebDriver to scrape bus information from Paytm's website,
providing a programmatic interface to access bus booking data.

Modules:
    generate_url: Contains functions for generating Paytm bus URLs and scraping bus data
    xpath: Contains XPath selectors for scraping bus information

Functions:
    generate_paytm_bus_url(source: str, destination: str, journey_date: str) -> dict:
        Generate a Paytm bus search URL and return bus information for the specified route.

Example:
    >>> from paytmbus import generate_paytm_bus_url
    >>> result = generate_paytm_bus_url("Bangalore", "Pune", "2025-03-01")
    >>> print(result)

Dependencies:
    - selenium: For web automation
    - json: For data serialization
    - datetime: For date validation

Note:
    This package requires Chrome browser and ChromeDriver to be installed on the system.
    The scraping functionality may be affected by changes to Paytm's website structure.
"""

from .generate_url import generate_paytm_bus_url
from .xpath import *

__version__ = "0.1.0"

__all__ = ['generate_paytm_bus_url']