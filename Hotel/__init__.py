"""
Hotel Package Documentation
=========================

This package provides functionality for scraping and processing hotel information from various booking platforms.
Currently supported platforms:
- Booking.com

Package Structure
----------------
Hotel/
├── __init__.py      # Package initialization and documentation
├── booking.py       # Booking.com scraper implementation
└── xpath.py         # XPath and CSS selectors for web scraping

Dependencies
-----------
- selenium: For web automation and scraping
- json: For data serialization
- time: For handling delays and timeouts

Usage Examples
-------------
1. Basic hotel search:
    from Hotel import scrape_hotels
    
    hotels = scrape_hotels(
        location="Goa",
        checkin="2025-02-12",
        checkout="2025-02-16"
    )

2. Advanced search with parameters:
    hotels = scrape_hotels(
        location="Mumbai",
        checkin="2025-03-01",
        checkout="2025-03-05",
        no_adults=2,
        no_rooms=1,
        no_children=1
    )

3. Save results to JSON:
    import json
    
    with open('hotels_data.json', 'w', encoding='utf-8') as f:
        json.dump(hotels, f, ensure_ascii=False, indent=4)

Data Structure
-------------
The scraper returns data in the following format:
{
    "type": "booking",
    "data": [
        {
            "title": "Hotel Name",
            "price": "1234",
            "review count": "100",
            "review comment": "Sample review text",
            "rating": "4.5",
            "image_url": "https://example.com/image.jpg",
            "hotel url": "https://booking.com/hotel/...",
            "Breakfast included": "True/False"
        },
        ...
    ]
}

Error Handling
-------------
The package implements robust error handling for various scenarios:
- TimeoutException: When page elements take too long to load
- NoSuchElementException: When required elements are not found
- General exceptions: For unexpected errors during scraping

Performance Considerations
------------------------
1. The scraper uses Selenium WebDriver with Chrome
2. Implements dynamic scrolling to load more results
3. Limits results to 10 hotels by default
4. Includes 2-second delays between scrolls for stability


Maintenance
----------
The package is designed for easy maintenance:
- All selectors are centralized in xpath.py
- Modular design allows for easy addition of new features
- Comprehensive documentation for all components

Version History
--------------
0.1.0 (Initial Release)
- Basic Booking.com scraping functionality
- JSON output support
- Error handling implementation

Future Enhancements
------------------
1. Support for additional booking platforms
2. Advanced filtering options
3. Price comparison features
4. Booking availability checking
5. User reviews analysis

Contributing
-----------
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.
"""

from .booking import scrape_hotels

__version__ = "1.0.0"

__all__ = ['scrape_hotels']

# Package-level configuration
DEFAULT_TIMEOUT = 20  # seconds
MAX_HOTELS = 10
SCROLL_DELAY = 2  # seconds
SCROLL_STEP = 1000  # pixels

# Export version and configuration
__version_info__ = tuple(map(int, __version__.split('.')))
