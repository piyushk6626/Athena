from airbnb.airbnb_func import *


data = scrape_airbnb("pune", "2025-03-09", "2025-03-11", "1", "0")
print(json.dumps(data, indent=2))