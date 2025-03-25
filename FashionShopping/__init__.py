"""
FashionShopping Package
----------------------
A Python package for interacting with the Carter API to search and retrieve fashion items.
This package provides a simple interface for making fashion-related queries and handling
API responses in a standardized format.

Features:
    - Text-based fashion item search
    - Automatic response data normalization
    - Configurable API settings
    - Error handling for API requests

Main Components:
    - fashion_search_api: Main function for searching fashion items
    - API_CONFIG: Configuration settings for the Carter API
    - Response normalization utilities

Configuration:
    The package uses a default configuration stored in API_CONFIG:
    - base_url: The base URL for the Carter API
    - default_results: Default number of results to return

Example Usage:
    Basic search:
    >>> from FashionShopping import fashion_search_api
    >>> results = fashion_search_api("summer dresses")
    
    Search with custom result count:
    >>> detailed_results = fashion_search_api("vintage jeans", number_of_results=10)

Returns:
    Search results are returned as a dictionary with:
    - type: The type of search performed ("fashion")
    - data: List of normalized fashion items
"""

from .carter import fashion_search_api, API_CONFIG

__version__ = "0.1.0"

__all__ = [
    "fashion_search_api",
    "API_CONFIG"
]