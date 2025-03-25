"""
FlightCompare Package
--------------------
A package for comparing flight prices across different providers using web scraping.

Main components:
- Flight search functionality: Search for flights between cities using IATA codes
- Airport code handling: Load and manage airport IATA codes
- Web scraping utilities: Selenium-based scraping of flight information
- XPath definitions: Structured XPath expressions for web scraping

Features:
- Search flights between cities
- Compare prices across multiple providers
- Get detailed flight information including:
  * Departure and arrival times
  * Flight duration
  * Number of stops
  * Airline information
  * Multiple provider options
  * Direct booking links
"""

from .searchflight import search_flight_url
from .xpaths import *

__version__ = "0.1.0"

# Export main functions and constants
__all__ = [
    'search_flight_url',    
]
