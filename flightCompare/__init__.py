"""
FlightCompare Package
--------------------
A comprehensive flight price comparison tool that scrapes and analyzes flight data
across multiple providers using automated web scraping techniques.

Core Components
-------------
1. Flight Search Engine:
   - Search flights between cities using IATA codes
   - Support for multiple date formats
   - Flexible city name matching

2. Airport Management:
   - IATA code handling and validation
   - Airport code database integration
   - City name to airport code mapping

3. Web Scraping Infrastructure:
   - Selenium-based automated scraping
   - Dynamic content handling
   - Resilient error management
   - Multiple provider support

4. Data Processing:
   - Standardized flight data format
   - Price normalization
   - Duration parsing
   - Multi-currency support

Features
--------
- Comprehensive flight search across providers
- Real-time price comparison and tracking
- Detailed flight information including:
  * Precise departure and arrival times
  * Flight duration calculation
  * Layover information and stop counts
  * Airline details with logos
  * Multiple fare options
  * Direct booking links to providers
  * Price history (when available)
  * Fare class information
  * Baggage allowance details

Usage Examples
------------
Basic flight search:
    >>> from flightCompare import search_flight_url
    >>> results = search_flight_url("New York", "London", "2024-05-01")

Technical Details
---------------
- Requires Chrome WebDriver
- Supports Python 3.7+
- Implements automatic retry mechanisms
- Handles rate limiting and anti-bot measures
- Thread-safe operations

Error Handling
------------
The package implements comprehensive error handling for:
- Network timeouts
- Invalid airport codes
- Missing flight data
- Scraping failures
- Browser automation issues
"""

from .searchflight import (
    search_flight_url,
    scrape_flights,
    load_airport_codes
)
from .xpaths import *

# Package metadata
__version__ = "0.1.0"

# Export public API
__all__ = [
    'search_flight_url',
    'scrape_flights',
    'load_airport_codes',
]

# Package configuration
DEFAULT_TIMEOUT = 20  # Default timeout for web requests in seconds
MAX_RETRIES = 3      # Maximum number of retry attempts
USER_AGENT = "FlightCompare/0.1.0"  # Default user agent for requests
