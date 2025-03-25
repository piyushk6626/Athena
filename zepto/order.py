"""
Zepto Order Scraping Module

This module provides functionality to scrape product information from Zepto's website.
It uses Selenium WebDriver to automate the browser and extract product details.

The module implements a headless browser approach to scrape product information,
including URLs, images, names, subtitles, and prices. It handles errors gracefully
and limits results to 10 items per search query.

Dependencies:
    - selenium: For web automation and element selection
    - webdriver_manager: For automatic ChromeDriver management

Note:
    This module requires Chrome browser to be installed on the system.
    It uses headless mode by default for better performance.

Example:
    >>> from zepto import scrape_zepto
    >>> results = scrape_zepto("milk")
    >>> print(results)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .xpath import (
    PRODUCT_CARD,
    PRODUCT_IMAGE,
    PRODUCT_NAME,
    PRODUCT_SUBTITLE,
    PRODUCT_PRICE
)


def scrape_zepto(query):
    """
    Scrapes Zepto search results for the given query and returns a list of dictionaries containing product details.

    This function performs the following operations:
    1. Initializes a headless Chrome browser
    2. Navigates to Zepto's search page with the given query
    3. Extracts product information from the search results
    4. Returns formatted data in a structured dictionary

    Args:
        query (str): The search query to scrape results for.
                    This can be any product name or category.

    Returns:
        dict: A dictionary with the following structure:
            {
                "type": str,  # Either "zepto" or "text" depending on results
                "data": Union[List[Dict], str]  # Either list of product dicts or error message
                    If successful, each product dict contains:
                    {
                        "url": str,      # URL of the product page
                        "img": str,      # URL of the product image
                        "name": str,     # Name of the product
                        "subtitle": str, # Subtitle/description of the product
                        "price": str     # Price of the product
                    }
            }

    Note:
        - The function limits results to 10 items per search
        - If no items are found, returns a text message instead of product data
        - All fields in the product dictionary may be None if extraction fails
        - The browser is automatically closed after scraping

    Raises:
        selenium.common.exceptions.WebDriverException: If browser initialization fails
        selenium.common.exceptions.TimeoutException: If page load times out
    """
    # Initialize Chrome options for headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for better performance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Construct the search URL with the provided query
        url = f"https://www.zeptonow.com/search?query={query}"
        driver.get(url)  

        # Find all product cards on the page using the predefined XPath
        elements = driver.find_elements(By.XPATH, PRODUCT_CARD)
        
        data = []
        for element in elements:
            item = {}
            
            # Extract URL from the product card link
            try:
                item['url'] = element.get_attribute('href')
            except:
                item['url'] = None
            
            # Extract image source from the product card
            try:
                img_element = element.find_element(By.XPATH, PRODUCT_IMAGE)
                item['img'] = img_element.get_attribute('src')
            except:
                item['img'] = None
                
            # Extract product name from the card
            try:
                name_element = element.find_element(By.XPATH, PRODUCT_NAME)
                item['name'] = name_element.text
            except:
                item['name'] = None
                
            # Extract product subtitle/description
            try:
                subtitle_element = element.find_element(By.XPATH, PRODUCT_SUBTITLE)
                item['subtitle'] = subtitle_element.text
            except:
                item['subtitle'] = None
                
            # Extract product price
            try:
                price_element = element.find_element(By.XPATH, PRODUCT_PRICE)
                item['price'] = price_element.text
            except:
                item['price'] = None
            
            data.append(item)

            # Limit results to 10 items for performance and consistency
            if(len(data) == 10):
                break

        # Format the response based on whether data was found
        if data == []:
            final = {
                "type": "text",
                "data": "No Item found."
            }
        else:
            final = {
                "type": "zepto",
                "data": data
            }
        
        return final
    finally:
        driver.quit()

