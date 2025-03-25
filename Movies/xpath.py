"""
XPath constants used across the movie scraping modules.
These constants store all the XPath selectors used to locate elements on the Paytm movie booking website.
"""

# =============================================================================
# Movie List Page XPaths
# Used for scraping the main movie listing page
# =============================================================================
MOVIE_CARD = "//div[@class='DesktopRunningMovie_movieCard__p5n6P']"  # Container for each movie card
MOVIE_POSTER = ".//div[@class='DesktopRunningMovie_imgCon__XM_UA']/img"  # Movie poster image
MOVIE_LINK = ".//div[@class='DesktopRunningMovie_runningMovie__N17Hp']/a"  # Link to movie details
MOVIE_TITLE = ".//div[@class='DesktopRunningMovie_movTitle__Q1pOY']"  # Movie title text
MOVIE_AGE_RATING = ".//div[@class='DesktopRunningMovie_point__YtD_w']/span"  # Age rating (U/A, A, etc.)
MOVIE_LANGUAGE = ".//div[@class='DesktopRunningMovie_point__YtD_w']/span[@class='textClamp']"  # Movie language
VIEW_MORE_BUTTON = "//div[@class='ViewMore_viewAll__KJ5c1']/span"  # Button to load more movies
OVERLAY_BACKDROP = "//div[@class='Overlay_backdrop__F12DQ']"  # Overlay that appears on page load

# =============================================================================
# Movie Shows Page XPaths
# Used for scraping show timings and theater information
# =============================================================================
THEATER_SESSIONS = "//div[@class='MovieSessionsListingDesktop_movieSessions__KYv1d']"  # Container for theater listings
THEATER_NAME = ".//div[@class='MovieSessionsListingDesktop_details__Aq3st']/a"  # Theater name link
SHOW_TIMES = ".//div[contains(@class, 'MovieSessionsListingDesktop_timeblock__MiYNc')]"  # Container for show times
TIME_SLOT = ".//div[contains(@class, 'MovieSessionsListingDesktop_time__r6FAI')]"  # Individual show time
MOVIE_FORMAT = ".//div[@class='MovieSessionsListingDesktop_premiumLabel__ed70A']"  # Movie format (2D, 3D, etc.)

# =============================================================================
# Seat Layout Page XPaths
# Used for scraping and interacting with the seat selection page
# =============================================================================
LAYOUT_CONTAINERS = '//div[@class="FixedSeatingDesktop_layoutCon__vNrYG"]'  # Container for seat sections
SEAT_TYPE_PRICE = './/div[@class="FixedSeatingDesktop_detaDetail__5yNOt"]/div'  # Seat type and price info
SEAT_ROWS = './/div[@class="FixedSeatingDesktop_rightRow__FnHaS"]/ul/li'  # Container for each row
ROW_NUMBER = './/div[@class="FixedSeatingDesktop_seatName__m6_Hm"]'  # Row number/name
SEATING_ELEMENT = './/div[@class="FixedSeatingDesktop_seatL__uU4Pm"]'  # Container for seats in a row
BOOK_TICKET_BUTTON = "//button[contains(@class, 'SeatLayoutFooterDesktop_bookTicket')]"  # Book ticket button
QR_CONTAINER = "//div[contains(@class, 'qrContainer')]"  # Payment QR code container

# =============================================================================
# City Selection XPaths
# Used for city selection functionality
# =============================================================================
CITY_SEARCH_INPUT = "input.AnimatedSearchBar_animInput__iuqxe"  # City search input field
CITY_DROPDOWN = '//div[@class="DesktopMovieCitySelector_cityListing__tz4Zf"]'  # City dropdown container
FIRST_CITY_RESULT = '(//div[@class="fullHeightScrollDweb DesktopMovieCitySelector_dropdown__PE__h"])[1]'  # First city in dropdown

# =============================================================================
# Language Selection XPaths
# Used for language selection functionality
# =============================================================================
LANG_CONTAINER = "LanguageSelectionDialog_langSelectionContainer__jZY7u"  # Language selection container
LANG_RADIO = "//input[@value='{language}-index']"  # Language radio button (format string)
PROCEED_BUTTON = "LanguageSelectionDialog_applyBtn__2frJM"  # Proceed button after language selection 