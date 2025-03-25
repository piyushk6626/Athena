"""
XPath selectors for Zepto web scraping.
This module contains all the XPath selectors used in the Zepto scraping functionality.
"""

# Main product card selector
PRODUCT_CARD = "//a[@class='!my-0 relative z-0 my-3 rounded-t-xl rounded-b-md group']"

# Product image selector
PRODUCT_IMAGE = ".//div[@class='relative z-0 rounded-xl bg-gray-200']/div[@class='overflow-hidden rounded-xl border-[0.5px] border-gray-200']/img"

# Product name selector
PRODUCT_NAME = ".//h5[@data-testid='product-card-name']"

# Product subtitle selector
PRODUCT_SUBTITLE = ".//h4[@class='font-heading text-lg tracking-wide line-clamp-1 mt-1 !text-sm !font-normal flex items-center']"

# Product price selector
PRODUCT_PRICE = ".//h4[@data-testid='product-card-price']" 