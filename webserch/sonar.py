"""
Module for web search functionality using Perplexity AI's Sonar API.

This module provides functionality to search the web for news and information
using Perplexity AI's Sonar API. It handles API authentication, request formatting,
and response processing.

Dependencies:
    - openai: For interacting with Perplexity AI API
    - python-dotenv: For loading environment variables
    - os: For accessing environment variables

Example:
    >>> result = serach_the_web_for_news("What are the latest developments in AI?")
    >>> print(result['type'])
    'perplexity'
"""

from openai import OpenAI
from dotenv import load_dotenv
import os


def serach_the_web_for_news(query: str) -> dict:
    """
    Search the web for news using Perplexity AI Sonar API.

    This function takes a search query and returns relevant information from the web
    using Perplexity AI's Sonar API. It processes the response and formats it into
    a structured dictionary containing the response content and cited URLs.

    Args:
        query (str): The search query string to find relevant information.

    Returns:
        dict: A dictionary containing:
            - type (str): The type of response, always "perplexity"
            - data (list): A list containing a single dictionary with:
                - response_content (str): The main content of the response
                - response_url (str): Comma-separated string of cited URLs

    Raises:
        ValueError: If the query string is empty or invalid.

    Example:
        >>> result = serach_the_web_for_news("Latest tech news")
        >>> print(result['type'])
        'perplexity'
    """
    
    # Load environment variables from .env file
    load_dotenv(override=True)
    PRELEXITY_API_KEY = os.getenv("PRELEXITY_API_KEY")

    # Define the conversation messages for the API
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {   
            "role": "user",
            "content": query,
        },
    ]

    # Initialize the OpenAI client with Perplexity AI configuration
    client = OpenAI(
        api_key=PRELEXITY_API_KEY,
        base_url="https://api.perplexity.ai"
    )

    # Make the API request for chat completion
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )

    # Extract response content and citations
    response_content = response.choices[0].message.content
    response_url = response.citations
    
    # Join URLs with commas for storage
    result = ",".join(response_url)
    
    # Format the response into the expected structure
    response_dict = {
        "type": "perplexity",
        "data": [{
            "response_content": response_content,
            "response_url": result
        }]
    }
    
    return response_dict
