# destination = ""
# checkinDate = ""
# checkoutDate = ""
# adultsNo = ""
# childrenNo = ""
# url = https://www.airbnb.co.in/s/{destination}/homes?refinement_paths%5B%5D=%2Fhomes&place_id=ChIJQbc2YxC6vzsRkkDzYv-H-Oo&checkin={checkinDate}&checkout={checkoutDate}&adults={adultsNo}&children={childrenNo}&query={destination}&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-03-01&monthly_length=3&monthly_end_date=2025-06-01&search_mode=regular_search&price_filter_input_type=0&price_filter_num_nights=1&channel=EXPLORE&ne_lat=16.556983681206173&ne_lng=76.26666657104118&sw_lat=14.133389738197371&sw_lng=71.5802091689477&zoom=9.554526026357014&zoom_level=9.554526026357014&search_by_map=true&search_type=user_map_move

# xpath = //div[@ class="c4mnd7m atm_9s_11p5wf0 atm_dz_1osqo2v dir dir-ltr"]

#xpath for image of the hotel with every photos 
#//div/picture/img[@class="i1ezuexe atm_e2_idpfg4 atm_vy_idpfg4 atm_mk_stnw88 atm_e2_1osqo2v_1lzdix4 atm_vy_1osqo2v_1lzdix4 i1wndum8 atm_jp_pyzg9w atm_jr_nyqth1 i16t4q3z atm_vh_yfq0k3 dir dir-ltr"]

# xpath for tag 
#//div[@class="t1qa5xaj dir dir-ltr"]

# xpath for detail of the rooms 
#//div[@class='g1qv1ctd atm_u80d3j_1li1fea atm_c8_o7aogt atm_g3_8jkm7i c1v0rf5q atm_9s_11p5wf0 atm_cx_4wguik atm_dz_7esijk atm_e0_1lo05zz dir dir-ltr']
#xpath for location of apartment
#//div[@class='t1jojoys atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_1vgr820 atm_7l_jt7fhx atm_cs_10d11i2 atm_w4_1eetg7c atm_ks_zryt35__1rgatj2 dir dir-ltr']
#xpath for detail of room 
# //div[@class='fb4nyux atm_da_cbdd7d s1cjsi4j atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_kb7nvz atm_7l_1he744i atm_ks_zryt35__1rgatj2 dir dir-ltr']
#xpath for price 
# //div[@class="pquyp1l atm_da_cbdd7d pi11895 atm_h3_lh1qj6 dir dir-ltr"]
#xpath of total price 
#//div[@class="_tt122m"]
#xpath for rating 
#//span[@class="r4a59j5 atm_h_1h6ojuz atm_9s_1txwivl atm_7l_jt7fhx atm_84_evh4rp atm_mk_h2mmj6 atm_mj_glywfm dir dir-ltr"]/span[@aria-hidden="true"]

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
#//div/button[@data-testid="homes-pdp-cta-btn"]\
#xpath for location 
#//div/span[@class="t6mzqp7 atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_kb7nvz atm_7l_1he744i atm_am_qk3dho atm_ks_zryt35__1rgatj2 dir dir-ltr"]


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from urllib.parse import urlparse, parse_qs

# Initialize Chrome options
chrome_options = Options()
# Remove the headless mode to run the browser with a GUI
# chrome_options.add_argument("--headless")  # Do not run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Automatically manage ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the search parameters
destination = "goa"
checkinDate = "2025-02-09"
checkoutDate = "2025-02-14"
adultsNo = "1"
childrenNo = "0"

url = f"https://www.airbnb.co.in/s/{destination}/homes?checkin={checkinDate}&checkout={checkoutDate}&adults={adultsNo}&children={childrenNo}&query={destination}"

# Navigate to the URL
driver.get(url)
time.sleep(5)  # Wait for the page to load

# List to store all hotel data
hotels_data = []

# Function to extract hotel data from the current page
def extract_hotels():
    hotels = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')

    for hotel in hotels:
        try:
            # Extract hotel details
            images = [img.get_attribute('src') for img in hotel.find_elements(By.XPATH, './/div/picture/img')]
            hotel_name = hotel.find_element(By.XPATH, './/div[contains(@class, "t1jojoys")]').text
            hotel_url = hotel.find_element(By.XPATH, './/a[contains(@class, "l1ovpqvx")]').get_attribute('href')
            location_details = hotel.find_element(By.XPATH, './/div[contains(@class, "g1qv1ctd")]').text
            price = hotel.find_element(By.XPATH, './/div[contains(@class, "pquyp1l")]').text
            total_price = driver.find_element(By.XPATH, '//div[@class="_tt122m"]').text
            ratings = hotel.find_element(By.XPATH, './/span[contains(@class, "r4a59j5")]/span[@aria-hidden="true"]').text
            room_tag = driver.find_element(By.XPATH, '//div[@class="t1qa5xaj dir dir-ltr"]').text
            paymentlink= driver.find_element(By.XPATH, '//div/a[@class="l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 bn2bl2p atm_5j_223wjw atm_9s_1ulexfb atm_e2_1osqo2v atm_fq_idpfg4 atm_mk_stnw88 atm_tk_idpfg4 atm_vy_1osqo2v atm_26_1j28jx2 atm_3f_glywfm atm_kd_glywfm atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_aaiy6o_1w3cfyq_oggzyc atm_70_1b8lkes_1w3cfyq_oggzyc atm_uc_glywfm_1w3cfyq_pynvjw atm_uc_aaiy6o_pfnrn2_ivgyl9 atm_70_1b8lkes_pfnrn2_ivgyl9 atm_uc_glywfm_pfnrn2_61fwbc dir dir-ltr"]').get_attribute("href")

            # Store data in a dictionary
            hotel_info = {
                "images": images,
                "hotel_name": hotel_name,
                "hotel_url": hotel_url,
                "location": location_details,
                "price": price,
                "total price":total_price,
                "ratings": ratings,
                "room_tag":room_tag,
                "payment_link":paymentlink,
            }

            hotels_data.append(hotel_info)

        except Exception as e:
            print(f"Error extracting data for a hotel: {e}")

# Loop through pages and extract data
# while True:
    
#     extract_hotels()
#     # Try to find the "Next" page or pagination cursor
#     next_button = driver.find_elements(By.XPATH, '//a[@aria-label="Next"]')
#     if next_button:
#         cursor = next_button[0].get_attribute('href')  # Get next page cursor
#         cursor = parse_qs(urlparse(cursor).query).get('cursor', [None])[0]  # Extract cursor
#         if cursor:
#             # Go to the next page using the cursor (pagination)
#             driver.get(f"{url}&cursor={cursor}")
#             time.sleep(8)  # Wait for the page to load
#         else:
#             break  # Stop if no cursor is found (end of pages)
#     else:
#         break  # No next page, stop the loop

extract_hotels()

# Close the WebDriver
driver.quit()

# Save data in JSON format
response_dict = {
    'type' : 'airbnb',
    'data' : hotels_data
}

print(f"Scraped data for {len(hotels_data)} hotels and saved to {hotels_data}")
