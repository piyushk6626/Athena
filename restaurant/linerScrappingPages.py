"""
Linear Scraping Module for Google Maps Restaurant Pages

This module provides functionality to scrape restaurant data from Google Maps pages sequentially.
It processes each restaurant URL from a CSV file, extracts relevant information including:
- Basic restaurant details (name, rating, location)
- Restaurant images
- Customer tags and their frequencies
- Customer reviews with photos
- Saves the data to individual JSON files

Dependencies:
    - selenium: For web scraping
    - csv: For reading input data
    - json: For saving scraped data
    - time: For handling delays and timestamps
"""

# YOU HAVE A CSV LIKE THIS 
# Name,Star,Number,AREA,URL
# Filomena's Kitchen,4.4,532,"Airport, Dabolim",https://www.google.com/maps/search/Filomena%27s+Kitchen+Airport%2C+Dabolim
# Joet's Bar & Restaurant,4.1,3200,"Airport, Dabolim",https://www.google.com/maps/search/Joet%27s+Bar+%26+Restaurant+Airport%2C+Dabolim

# OPEN THE URL AND SCRAP THE DATA


# RESTURENT IMAGE = //div[@class="RZ66Rb FgCUCc"]/button/img
# REVIEW BUTTON //button[@class="hh2c6 G7m0Af"]      

# TAGS 
# Parent ELEMENT //div[@class="tXNTee "]
# TAG //div[@class="tXNTee "]/span[@class="uEubGf fontBodyMedium"]
# TAG COUNT  //div[@class="tXNTee "]/span[@class="bC3Nkc fontBodySmall"]

#SAVE 5-10 REVIEWS
 
# REVIEWS 
# PARENT ELEMENT //div[@class="jftiEf fontBodyMedium "]
# CLICK THE READ MORE BUTTON //button[@class="w8nwRe kyuRq"]
# READ THE REVIEW //span[@class="wiI7pd"]
# LIST OF PHOTO //div[@class="KtCyie"]
# EACH ONE IS LIKE FOLLOWING HTML SCPRE THE LINK FORM IT <button class="Tya61d" data-photo-index="0" data-review-id="ChdDSUhNMG9nS0VJQ0FnSUR2eTg2UC1BRRAB" data-tooltip="" jsaction="pane.wfvdle165.review.openPhoto;keydown:pane.wfvdle165.review.openPhoto;focus:pane.focusTooltip;blur:pane.blurTooltip" aria-label="Photo 1 on Sasikumar krishnan's review" style="background-image: url(&quot;https://lh3.googleusercontent.com/geougc-cs/AHRlGdnAPDSD_Lo5Sb4IsKb0ljUg7B_1EpFR5QtPbgla1gibw2Q_ycJqG25iiuZfPpstbJYoBMABPnn1AJG_7MlIj55fmUVnhhDkeh3QCtYNTsfieDr1yCg4LaqjB56jZjpe4mB9RrE=w338-h253-p&quot;); width: calc(50% - 1px); padding-top: calc(37.5% - 1px); margin-right: 2px;"></button> 

# SAVE THIS TO A JSON FILE

import csv
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .xpath import (
    RESTAURANT_IMAGE,
    REVIEW_BUTTON,
    TAG_PARENT,
    TAG_NAME,
    TAG_COUNT,
    REVIEW_PARENT,
    READ_MORE_BUTTON,
    REVIEW_TEXT,
    PHOTO_CONTAINER,
    PHOTO_BUTTON
)

def get_driver():
    """
    Create and configure a new Chrome WebDriver instance.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance with headless mode enabled.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run browser in headless mode
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_place(row, counter):
    """
    Scrape data from a single Google Maps restaurant page.
    
    Args:
        row (dict): Dictionary containing restaurant information from CSV
        counter (int): Counter for generating unique IDs
        
    Returns:
        dict: Dictionary containing scraped restaurant data including:
            - Basic info (name, rating, location)
            - Restaurant image URL
            - Customer tags with frequencies
            - Customer reviews with photos
    """
    # Initialize data dictionary with basic restaurant information
    data = {
        "id": None,
        "name": row["Name"],
        "star": row["Star"],
        "number": row["Number"],
        "score": row['Score'],
        "area": row["AREA"],
        "url": row["URL"],
        "restaurant_image": None,
        "tags": [],
        "reviews": []
    }
    
    # Generate unique ID using timestamp and counter
    timestamp = time.strftime("%Y%m%d%H%M%S")
    scrape_id = f"{timestamp}_{counter}"
    data["id"] = scrape_id

    # Initialize WebDriver and wait object
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        # Load and refresh the page to ensure proper URL
        driver.get(row["URL"])
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        data["url"] = driver.current_url
    except Exception as e:
        print(f"Error loading {row['URL']}: {e}")
        driver.quit()
        return data
    
    # Extract restaurant image
    try:
        img_elem = wait.until(EC.presence_of_element_located((By.XPATH, RESTAURANT_IMAGE)))
        data["restaurant_image"] = img_elem.get_attribute("src")
    except Exception as e:
        print(f"Restaurant image not found for {row['Name']}: {e}")

    # Open reviews panel
    try:
        review_button = wait.until(EC.element_to_be_clickable((By.XPATH, REVIEW_BUTTON)))
        review_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Review button not clickable for {row['Name']}: {e}")
        driver.quit()
        return data

    # Extract customer tags
    try:
        tag_containers = driver.find_elements(By.XPATH, TAG_PARENT)
        for container in tag_containers:
            try:
                tag_name = container.find_element(By.XPATH, TAG_NAME).text
                tag_count = container.find_element(By.XPATH, TAG_COUNT).text
                if tag_name and tag_count:
                    data["tags"].append({"tag": tag_name, "count": tag_count})
            except Exception as inner_e:
                continue
    except Exception as e:
        print(f"Tags not found for {row['Name']}: {e}")

    # Extract reviews (up to 10)
    try:
        review_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, REVIEW_PARENT)))
        
        for review_elem in review_elements[:10]:
            review_data = {}

            # Expand review text if "Read more" button exists
            try:
                read_more = review_elem.find_element(By.XPATH, READ_MORE_BUTTON)
                if read_more.is_displayed():
                    driver.execute_script("arguments[0].click();", read_more)
                    time.sleep(0.5)
            except Exception:
                pass

            # Extract review text
            try:
                review_text_elem = review_elem.find_element(By.XPATH, REVIEW_TEXT)
                review_data["review_text"] = review_text_elem.text
            except Exception as e:
                review_data["review_text"] = ""
                print(f"Could not extract review text for a review in {row['Name']}: {e}")

            # Extract review photos
            photos = []
            try:
                photo_container = review_elem.find_element(By.XPATH, PHOTO_CONTAINER)
                photo_buttons = photo_container.find_elements(By.XPATH, PHOTO_BUTTON)
                for button in photo_buttons:
                    style = button.get_attribute("style")
                    m = re.search(r'url\(["\']?(.*?)["\']?\)', style)
                    if m:
                        photos.append(m.group(1))
            except Exception:
                pass
            review_data["photos"] = photos

            data["reviews"].append(review_data)
    except Exception as e:
        print(f"Error extracting reviews for {row['Name']}: {e}")

    driver.quit()
    return data

def main():
    """
    Main function to process restaurant data from CSV file.
    
    Reads restaurant URLs from input.csv, scrapes data for each restaurant,
    saves individual JSON files, and creates an updated CSV with IDs.
    """
    input_csv = "input.csv"
    output_csv = "updated_input.csv"
    updated_rows = []
    counter = 1

    import os
    output_folder = "scraped_data4"
    os.makedirs(output_folder, exist_ok=True)

    # Process each restaurant from CSV
    with open(input_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"Scraping: {row['Name']}")
            data = scrape_place(row, counter)
            
            # Save scraped data to JSON file
            json_filename = os.path.join(output_folder, f"scrape_{data['id']}.json")
            with open(json_filename, "w", encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, indent=4, ensure_ascii=False)
            
            # Update CSV row with ID
            row["ID"] = data["id"]
            updated_rows.append(row)
            counter += 1
            
    # Save updated CSV with IDs
    fieldnames = list(updated_rows[0].keys())
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
    
    print("Scraping complete. Individual JSON files created and updated CSV saved.")

if __name__ == "__main__":
    main()
