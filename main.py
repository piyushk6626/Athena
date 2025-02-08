
from Movies import (
    scrape_movies,
    extract_movie_shows,
    extract_seat_details,
    select_given_seat_and_click_book_ticket,
)

# Example: Scrape movies in a city.
movies_json = scrape_movies("pune")
print(movies_json)

#Example: Extract show details.
shows = extract_movie_shows("https://paytm.com/movies/interstellar-2014-movie-detail-288?frmtid=zrwlluqk8", "pune", "english")
print(shows)


url, seat_details = extract_seat_details("https://paytm.com/movies/interstellar-2014-movie-detail-288?frmtid=zrwlluqk8", "pune", "english", "PVR Directors Cut KOPA, KOPA Mall, Pune", "07:30 PM")
print(seat_details)

# Example: Book seats and capture payment screenshot.
seat_data, screenshot = select_given_seat_and_click_book_ticket(
    "https://paytm.com/movies/seat-layout/pune/zrwlluqk8?encsessionid=1027604-10985-o9nvqc-1027604&freeseating=false&fromsessions=true",
    seat_rows=["B", "B"],
    seat_numbers=[3, 4]
)
print(seat_data, screenshot)
