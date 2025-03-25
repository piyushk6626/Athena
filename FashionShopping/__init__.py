"""
FashionShopping Package
----------------------
A package for searching and retrieving fashion items using the Carter API.

Main components:
- Fashion search functionality through Carter API
- API configuration management
- Response data normalization

Example:
    >>> from FashionShopping import fashion_search_api
    >>> results = fashion_search_api("summer dresses")
"""

from .carter import fashion_search_api, API_CONFIG

__version__ = "0.1.0"

__all__ = [
    "fashion_search_api",
    "API_CONFIG"
]