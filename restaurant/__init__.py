"""
Athena Restaurant Data Collection and Analysis Package

This package provides functionality for scraping, processing, and analyzing restaurant data from Google Maps.
It includes tools for:
- Scraping restaurant information from Google Maps
- Processing and storing restaurant data
- Generating embeddings for semantic search
- Searching restaurants using natural language queries
- Managing restaurant data in vector databases

Modules:
    linerScrappingPages.py: Linear scraping of Google Maps restaurant pages
    concurrentScreppingPages.py: Concurrent scraping of Google Maps restaurant pages
    ResturentDiscrption.py: Generation of restaurant descriptions using GPT
    search.py: Semantic search functionality for restaurants
    PincoeUpload.py: Vector database management for restaurant data
    xpath.py: XPath selectors for web scraping
    prompts.py: System prompts for GPT models

Dependencies:
    - selenium: For web scraping
    - openai: For GPT model interactions
    - pinecone: For vector database operations
    - python-dotenv: For environment variable management

Usage:
    from restaurant import search, PincoeUpload
    
    # Search for restaurants
    results = search.find_similar_items("Italian food in downtown")
    
    # Upload restaurant data to vector database
    PincoeUpload.upload_restaurant_folder(index, "restaurant_data")
"""

from . import search
from . import PincoeUpload
from . import linerScrappingPages
from . import concurrentScreppingPages
from . import ResturentDiscrption
from . import xpath
from . import prompts

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = [
    'search',
    'PincoeUpload',
    'linerScrappingPages',
    'concurrentScreppingPages',
    'ResturentDiscrption',
    'xpath',
    'prompts'
]
