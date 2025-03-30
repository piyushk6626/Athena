"""
Router Module for Athena Virtual Assistant

This module provides a central hub for routing function calls to their appropriate
implementations across different service categories. It organizes related functions 
into logical groups and handles the dispatching of requests to the correct handlers.
"""

import logging
from typing import Dict, Any, Optional, Union, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import utils

# ----- Import service modules by category -----

# Web and search related imports
from webserch import serach_the_web_for_news  # TODO: Fix typo in module name

# Travel and transportation services
from flightCompare import search_flight_url, scrape_flights
from airbnb import scrape_airbnb
from Hotel import scrape_hotels
from paytmbus import generate_paytm_bus_url

# Entertainment and media services
from Movies import scrape_movies, extract_movie_shows
from spotify import play_song, pause_playback, resume_playback

# Shopping and retail services
from FashionShopping import fashion_search_api
from zepto.order import scrape_zepto

# Food and restaurant services
from restaurant.search import find_similar_items

# Communication and productivity services
from emailAutomation import send_email, read_emails


# ----- Function routing registry -----

# Group functions by category for better organization and maintainability
FUNCTION_REGISTRY = {
    # Web search functions
    "serach_the_web_for_news": serach_the_web_for_news,
    
    # Travel and accommodation functions
    "scrape_airbnb": scrape_airbnb,
    "find_hotels": scrape_hotels,
    "search_flight_url": search_flight_url,
    "scrape_flights": search_flight_url,
    "get_bus_data": generate_paytm_bus_url,
    
    # Entertainment functions
    "scrape_movies": scrape_movies,
    "extract_single_movie_show": extract_movie_shows,
    "play_song": play_song,
    "pause_playback": pause_playback,
    "resume_playback": resume_playback,
    
    # Shopping and retail functions
    "fashion_search_api": fashion_search_api,
    "scrape_zepto": scrape_zepto,
    
    # Food and restaurant functions
    "find_similar_restaurants": find_similar_items,
    
    # Communication functions
    "send_email_tool": send_email,
    "send_email": send_email,
    "read_emails": read_emails,
}


def callfunction(name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Route a function call to the appropriate implementation based on the function name.
    
    This function serves as a central dispatcher that routes requests to the appropriate
    function handler based on the function name. It handles exceptions that might occur
    during function execution and provides proper logging.
    
    Args:
        name: The name of the function to call, which should match a key in FUNCTION_REGISTRY
        args: A dictionary of arguments to pass to the function
    
    Returns:
        The response from the called function or None if the function is not found
        
    Raises:
        Exception: If an error occurs during function execution
    """
    try:
        # Check if the function exists in our registry
        if name in FUNCTION_REGISTRY:
            logger.info(f"Routing call to function: {name}")
            handler = FUNCTION_REGISTRY[name]
            
            # Call the handler with the provided arguments
            response = handler(**args)
            logger.info(f"Function {name} executed successfully")
            
            return response
        else:
            logger.warning(f"Function {name} not found in registry")
            return utils.format_error_response(f"Function '{name}' not found in registry")
            
    except Exception as e:
        logger.error(f"Error executing function {name}: {e}")
        # Return an error response
        return utils.format_error_response(
            f"Error executing function {name}", 
            details=str(e)
        )


def call_multiple_functions(function_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Execute multiple function calls and return all their responses.
    
    Args:
        function_calls: A list of dictionaries, each containing:
                       - 'name': The name of the function to call
                       - 'args': A dictionary of arguments to pass to the function
    
    Returns:
        A dictionary containing all function responses keyed by function name.
        For multiple calls to the same function, responses will be numbered.
    """
    all_responses = {}
    function_counts = {}
    
    for call in function_calls:
        if 'name' not in call or 'args' not in call:
            logger.warning("Invalid function call format. Each call must include 'name' and 'args'")
            continue
        
        name = call['name']
        args = call['args']
        
        # Track how many times this function has been called
        if name in function_counts:
            function_counts[name] += 1
            response_key = f"{name}_{function_counts[name]}"
        else:
            function_counts[name] = 1
            response_key = name
            
        # Execute the function call
        response = callfunction(name, args)
        
        # Store the response
        all_responses[response_key] = response
    
    return utils.format_success_response(all_responses, "Multiple function calls executed")
    
if __name__ == "__main__":
    print(callfunction("scrape_airbnb", {"destination": "pune", "checkin_date": "2025-04-09", "checkout_date": "2025-04-14", "adults_no": "1", "children_no": "0"}))
    
    # Example of multiple function calls
    test_multiple_calls = [
        {
            "name": "serach_the_web_for_news",
            "args": {"query": "latest tech news"}
        },
        {
            "name": "scrape_airbnb",
            "args": {"destination": "pune", "checkin_date": "2025-04-09", "checkout_date": "2025-04-14", "adults_no": "1", "children_no": "0"}
        }
    ]
    print(call_multiple_functions(test_multiple_calls))
            
        
        












