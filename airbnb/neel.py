# destination = ""
# checkinDate = ""
# checkoutDate = ""
# adultsNo = ""
# childrenNo = ""
# url = https://www.airbnb.co.in/s/{destination}/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJQbc2YxC6vzsRkkDzYv-H-Oo&checkin={checkinDate}&checkout={checkoutDate}&adults={adultsNo}&children={childrenNo}&query={destination}&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-03-01&monthly_length=3&monthly_end_date=2025-06-01&search_mode=regular_search&price_filter_input_type=0&price_filter_num_nights=1&channel=EXPLORE&ne_lat=16.556983681206173&ne_lng=76.26666657104118&sw_lat=14.133389738197371&sw_lng=71.5802091689477&zoom=9.554526026357014&zoom_level=9.554526026357014&search_by_map=true&search_type=user_map_move

# xpath = //div[@ class="c4mnd7m atm_9s_11p5wf0 atm_dz_1osqo2v dir dir-ltr"]

#xpath for image of the hotel with every photos 
#//div/picture/img[@class="i1ezuexe atm_e2_idpfg4 atm_vy_idpfg4 atm_mk_stnw88 atm_e2_1osqo2v_1lzdix4 atm_vy_1osqo2v_1lzdix4 i1wndum8 atm_jp_pyzg9w atm_jr_nyqth1 i16t4q3z atm_vh_yfq0k3 dir dir-ltr"]

# xpath for detail of the rooms 
#//div[@class='g1qv1ctd atm_u80d3j_1li1fea atm_c8_o7aogt atm_g3_8jkm7i c1v0rf5q atm_9s_11p5wf0 atm_cx_4wguik atm_dz_7esijk atm_e0_1lo05zz dir dir-ltr']
#xpath for location of apartment
#//div[@class='t1jojoys atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_1vgr820 atm_7l_jt7fhx atm_cs_10d11i2 atm_w4_1eetg7c atm_ks_zryt35__1rgatj2 dir dir-ltr']
#xpath for detail of room 
# //div[@class='fb4nyux atm_da_cbdd7d s1cjsi4j atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_kb7nvz atm_7l_1he744i atm_ks_zryt35__1rgatj2 dir dir-ltr']
#xpath for price 
# //div[@class="pquyp1l atm_da_cbdd7d pi11895 atm_h3_lh1qj6 dir dir-ltr"]
#xpath for rating 
#//div[@class="t1a9j9y7 atm_da_1ko3t4y atm_dm_kb7nvz atm_fg_h9n0ih dir dir-ltr"]

#xpath for redirect to payment page 
#//div/a[@class="l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 bn2bl2p atm_5j_223wjw atm_9s_1ulexfb atm_e2_1osqo2v atm_fq_idpfg4 atm_mk_stnw88 atm_tk_idpfg4 atm_vy_1osqo2v atm_26_1j28jx2 atm_3f_glywfm atm_kd_glywfm atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_aaiy6o_1w3cfyq_oggzyc atm_70_1b8lkes_1w3cfyq_oggzyc atm_uc_glywfm_1w3cfyq_pynvjw atm_uc_aaiy6o_pfnrn2_ivgyl9 atm_70_1b8lkes_pfnrn2_ivgyl9 atm_uc_glywfm_pfnrn2_61fwbc dir dir-ltr"]


## for getting herf 
# from selenium import webdriver

# driver = webdriver.Chrome()
# driver.get("URL_OF_THE_PAGE")

# # Find the element using XPath and extract the href
# element = driver.find_element("xpath", '//div/a[contains(@class, "l1ovpqvx")]')
# href = element.get_attribute("href")

# print(href)
# driver.quit()


#redirect from checking page  to payment page 
#//div/button[@data-testid="homes-pdp-cta-btn"]


import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode, urlparse, parse_qs

# Function to construct URL dynamically
def construct_url_with_cursor(base_url, destination, checkin_date, checkout_date, adults, children, cursor=None):
    params = {
        "refinement_paths[]": "/homes",
        "checkin": checkin_date,
        "checkout": checkout_date,
        "adults": adults,
        "children": children,
        "query": destination,  # Use only the destination name
        "flexible_trip_lengths[]": "one_week",
        "search_mode": "regular_search",
        "price_filter_input_type": 0,
        "price_filter_num_nights": 1,
        "channel": "EXPLORE",
        "zoom": 9.5,
        "search_by_map": "true",
        "search_type": "user_map_move"
    }
    
    if cursor:
        params["cursor"] = cursor  # Add pagination cursor if available
    
    return base_url + "?" + urlencode(params)

# Setup the webdriver (WITHOUT headless mode)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keeps the browser open after script execution

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Take dynamic inputs
destination = input("Enter destination (e.g., Goa): ")
checkin_date = input("Enter check-in date (YYYY-MM-DD): ")
checkout_date = input("Enter check-out date (YYYY-MM-DD): ")
adults = input("Enter number of adults: ")
children = input("Enter number of children: ")

# Define the base URL for Airbnb search
base_url = f"https://www.airbnb.co.in/s/{destination}/homes"

# Initialize pagination cursor to None for the first page
cursor = None
all_data = []

# Loop through multiple pages
while True:
    url = construct_url_with_cursor(base_url, destination, checkin_date, checkout_date, adults, children, cursor)
    print(f"Fetching URL: {url}")  # Print URL for debugging
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(3)

    # Extract details using XPaths
    hotel_images = driver.find_elements(By.XPATH, '//div/picture/img[contains(@class, "i1ezuexe")]')
    rooms_details = driver.find_elements(By.XPATH, '//div[contains(@class, "g1qv1ctd")]')
    location_details = driver.find_elements(By.XPATH, '//div[contains(@class, "t1jojoys")]')
    room_prices = driver.find_elements(By.XPATH, '//div[contains(@class, "pquyp1l")]')
    room_ratings = driver.find_elements(By.XPATH, '//div[contains(@class, "t1a9j9y7")]')
    payment_redirect = driver.find_elements(By.XPATH, '//div/a[contains(@class, "l1ovpqvx")]')
    payment_button = driver.find_elements(By.XPATH, '//div/button[@data-testid="homes-pdp-cta-btn"]')

    # Collecting data in a dictionary
    data = {
        "hotel_images": [img.get_attribute('src') for img in hotel_images],
        "rooms_details": [room.text for room in rooms_details],
        "location_details": [location.text for location in location_details],
        "room_prices": [price.text for price in room_prices],
        "room_ratings": [rating.text for rating in room_ratings],
        "payment_redirect": [redirect.get_attribute("href") for redirect in payment_redirect],
        "payment_button": [button.get_attribute("aria-label") for button in payment_button]
    }
    
    all_data.append(data)

    # Try to find the "Next" page or pagination cursor
    next_button = driver.find_elements(By.XPATH, '//a[@aria-label="Next"]')
    if next_button:
        cursor = next_button[0].get_attribute('href')  # Get next page cursor
        cursor = parse_qs(urlparse(cursor).query).get('cursor', [None])[0]  # Extract cursor
        if not cursor:
            break  # Stop if no cursor is found
    else:
        break  # No next page, stop the loop

# Save all collected data into a JSON file
output_filename = f'hotel_data_{destination}.json'
with open(output_filename, 'w') as json_file:
    json.dump(all_data, json_file, indent=4)

print(f"Data saved to {output_filename}")

# Browser remains open for you to inspect manually
input("Press Enter to close the browser...")  # Keeps the browser open until you press Enter
driver.quit()
