"""
Zepto Package - Web Scraping Module for Zepto E-commerce Platform

This package provides a comprehensive solution for scraping product information
from Zepto's website. It implements a robust web scraping system using Selenium
WebDriver to automate browser interactions and extract detailed product data.

Package Structure:
    - order.py: Contains the main scraping functionality
    - xpath.py: Contains XPath selectors for element identification
    - __init__.py: Package initialization and exports

Features:
    - Headless browser automation for efficient scraping
    - Automatic ChromeDriver management
    - Graceful error handling and fallbacks
    - Structured data output in JSON format
    - Rate limiting and result pagination
    - Comprehensive product information extraction

Dependencies:
    - selenium>=4.0.0: For web automation and element selection
    - webdriver_manager>=3.8.0: For automatic ChromeDriver management
    - Chrome browser: Must be installed on the system

Usage Examples:
    Basic Usage:
        >>> from zepto import scrape_zepto
        >>> results = scrape_zepto("milk")
        >>> print(results)

    Advanced Usage with Error Handling:
        >>> try:
        ...     results = scrape_zepto("milk")
        ...     if results["type"] == "zepto":
        ...         for product in results["data"]:
        ...             print(f"Name: {product['name']}")
        ...             print(f"Price: {product['price']}")
        ... except Exception as e:
        ...     print(f"Error occurred: {e}")

Return Data Structure:
    {
        "type": str,  # Either "zepto" or "text"
        "data": Union[List[Dict], str]  # Product data or error message
            If successful, each product dict contains:
            {
                "url": str,      # Product page URL
                "img": str,      # Product image URL
                "name": str,     # Product name
                "subtitle": str, # Product description
                "price": str     # Product price
            }
    }

Notes:
    - The package uses headless mode by default for better performance
    - Results are limited to 10 items per search query
    - All fields in the product dictionary may be None if extraction fails
    - The browser is automatically closed after scraping
    - Rate limiting is implemented to prevent server overload

Limitations:
    - Requires Chrome browser installation
    - Internet connection required
    - May be affected by website changes or anti-scraping measures
    - Limited to publicly available product information

Version History:
    0.1.0 (2025-03-25):
        - Initial release
        - Basic product scraping functionality
        - Error handling and rate limiting
        - Structured data output


"""

from .order import scrape_zepto
from .xpath import *

__version__ = "0.1.0"

__license__ = "MIT"
__all__ = [
    "scrape_zepto"
]
