"""
This module contains all the XPath and CSS selectors used for scraping hotel information from Booking.com.
These selectors are used to locate and extract specific elements from the webpage.
"""

# Hotel container selector
HOTEL_CONTAINER = '//div[@class="c066246e13 d8aec464ca"]'

# Hotel details selectors
HOTEL_TITLE = 'div.f6431b446c'
REVIEW_COUNT = 'div.abf093bdfe.f45d8e4c32.d935416c47'
REVIEW_COMMENT = 'div.a3b8729ab1.e6208ee469.cb2cbb3ccb'
HOTEL_IMAGE = 'img.f9671d49b1'
HOTEL_URL = 'a.a78ca197d0'
BREAKFAST_INCLUDED = 'div.aaa3a3be2e' 