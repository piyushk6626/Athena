
# MVIE SCRAPEER DONE Fully
# from Movies import (
#     scrape_movies,
#     extract_movie_shows,
#     extract_seat_details,
#     select_given_seat_and_click_book_ticket,
# )

# # Example: Scrape movies in a city.
# movies_json = scrape_movies("mumbai")
# print(movies_json)

# #Example: Extract show details.
# shows = extract_movie_shows("https://paytm.com/movies/badass-ravi-kumar-movie-detail-166630", "mumbai", "hindi")
# print(shows)

# Example: Extract seat details.
# url, seat_details = extract_seat_details("https://paytm.com/movies/badass-ravi-kumar-movie-detail-166630", "mumbai", "hindi", "Cinepolis Viviana Mall, Eastern Express Highway, Thane", "09:05 AM")
# print(seat_details)

# # Example: Book seats and capture payment screenshot.
# seat_data, screenshot = select_given_seat_and_click_book_ticket(
#     "https://paytm.com/movies/seat-layout/pune/tu~7q2ziz6?encsessionid=1023543-25805-ob2oyk-1023543&freeseating=false&fromsessions=true",
#     seat_rows=["B", "B"],
#     seat_numbers=[3, 4]
# )
# print(seat_data, screenshot)
