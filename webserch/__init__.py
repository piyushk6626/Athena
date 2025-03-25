"""
Web Search Package

This package provides functionality for searching the web using various AI-powered APIs.
Currently, it supports Perplexity AI's Sonar API for web search and information retrieval.

Modules:
    sonar: Implements web search functionality using Perplexity AI's Sonar API

Classes:
    None

Functions:
    serach_the_web_for_news(query: str) -> dict:
        Search the web for news and information using Perplexity AI's Sonar API.

Example:
    >>> from webserch import serach_the_web_for_news
    >>> result = serach_the_web_for_news("Latest developments in AI")
    >>> print(result['type'])
    'perplexity'

Dependencies:
    - openai: For interacting with Perplexity AI API
    - python-dotenv: For loading environment variables
    - os: For accessing environment variables

Environment Variables:
    PRELEXITY_API_KEY: API key for Perplexity AI (required)

Version:
    0.1.0

"""

from .sonar import serach_the_web_for_news

__version__ = "0.1.0"

__all__ = [
    "serach_the_web_for_news",
]
