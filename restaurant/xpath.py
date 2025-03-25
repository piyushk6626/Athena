"""
This module contains all XPath selectors used for scraping Google Maps restaurant data.
These XPaths are used to locate and extract various elements from Google Maps restaurant pages.
"""

# Restaurant Image
RESTAURANT_IMAGE = '//div[@class="RZ66Rb FgCUCc"]/button/img'

# Review Button
REVIEW_BUTTON = '//button[@class="hh2c6 G7m0Af"]'

# Tags
TAG_PARENT = '//div[@class="tXNTee "]'
TAG_NAME = './/span[@class="uEubGf fontBodyMedium"]'
TAG_COUNT = './/span[@class="bC3Nkc fontBodySmall"]'

# Reviews
REVIEW_PARENT = '//div[@class="jftiEf fontBodyMedium "]'
READ_MORE_BUTTON = './/button[@class="w8nwRe kyuRq"]'
REVIEW_TEXT = './/span[@class="wiI7pd"]'
PHOTO_CONTAINER = './/div[@class="KtCyie"]'
PHOTO_BUTTON = './/button[contains(@class, "Tya61d")]' 