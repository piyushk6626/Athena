
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


