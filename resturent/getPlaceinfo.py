# Scrape EACH GOOLGLE MAPS PLACES  PAGE 

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
import os
import hashlib
import concurrent.futures

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define a global constant for the output folder.
OUTPUT_FOLDER = "scraped_data4"


def get_driver():
    """
    Create a new instance of the Chrome webdriver.
    Adjust options and the path to your chromedriver executable as needed.
    """
    options = webdriver.ChromeOptions()
    # Uncomment the next line if you want to run headless.
    options.add_argument("--headless")
    # You might need to specify the executable path if it's not in your PATH.
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_place(row, scrape_id):
    """
    Scrapes one Google Maps place page.
    
    Parameters:
      - row: A dictionary representing one CSV row.
      - scrape_id: A unique identifier (in our case, a hash string) for this place.
      
    The function:
      1. Uses the provided scrape_id.
      2. Opens a new browser instance, navigates to the URL, refreshes the page,
         and updates the URL from the browser.
      3. Extracts the restaurant image.
      4. Clicks the review button and extracts tags and up to 10 reviews.
         For each review, if a "Read more" button exists it clicks it,
         and then it extracts the review text and any photo URLs.
         
    Returns a dictionary of scraped data.
    """
    # Prepare the data dictionary with initial info from CSV.
    data = {
        "id": scrape_id,
        "name": row["Name"],
        "star": row["Star"],
        "number": row["Number"],
        "score": row.get("Score", ""),  # Use .get in case Score is missing.
        "area": row["AREA"],
        "url": row["URL"],  # Will be updated after refresh.
        "restaurant_image": None,
        "tags": [],
        "reviews": []
    }
    
    # Create a new driver instance for this URL.
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    
    try:
        # Open the URL and allow it to load.
        driver.get(row["URL"])
        time.sleep(2)
        
        # Refresh the page so that the browser obtains the "new" link.
        driver.refresh()
        time.sleep(2)
        
        # Update the URL in our data using the refreshed browser URL.
        data["url"] = driver.current_url
    except Exception as e:
        print(f"Error loading {row['URL']}: {e}")
        driver.quit()
        return data
    
    # --- SCRAPE THE RESTAURANT IMAGE ---
    try:
        img_elem = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="RZ66Rb FgCUCc"]/button/img')
        ))
        data["restaurant_image"] = img_elem.get_attribute("src")
    except Exception as e:
        print(f"Restaurant image not found for {row['Name']}: {e}")

    # --- OPEN THE REVIEWS PANEL ---
    try:
        review_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="hh2c6 G7m0Af"]')
        ))
        review_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Review button not clickable for {row['Name']}: {e}")
        driver.quit()
        return data

    # --- EXTRACT TAGS ---
    try:
        tag_containers = driver.find_elements(By.XPATH, '//div[@class="tXNTee "]')
        for container in tag_containers:
            try:
                tag_name = container.find_element(By.XPATH, './/span[@class="uEubGf fontBodyMedium"]').text
                tag_count = container.find_element(By.XPATH, './/span[@class="bC3Nkc fontBodySmall"]').text
                if tag_name and tag_count:
                    data["tags"].append({"tag": tag_name, "count": tag_count})
            except Exception:
                continue
    except Exception as e:
        print(f"Tags not found for {row['Name']}: {e}")

    # --- EXTRACT REVIEWS (up to 10) ---
    try:
        review_elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="jftiEf fontBodyMedium "]')
        ))
        
        for review_elem in review_elements[:10]:
            review_data = {}

            # Click the "Read more" button if present.
            try:
                read_more = review_elem.find_element(By.XPATH, './/button[@class="w8nwRe kyuRq"]')
                if read_more.is_displayed():
                    driver.execute_script("arguments[0].click();", read_more)
                    time.sleep(0.5)
            except Exception:
                # No "Read more" button for this review.
                pass

            # Extract the review text.
            try:
                review_text_elem = review_elem.find_element(By.XPATH, './/span[@class="wiI7pd"]')
                review_data["review_text"] = review_text_elem.text
            except Exception as e:
                review_data["review_text"] = ""
                print(f"Could not extract review text for a review in {row['Name']}: {e}")

            # Extract any attached photo URLs.
            photos = []
            try:
                photo_container = review_elem.find_element(By.XPATH, './/div[@class="KtCyie"]')
                photo_buttons = photo_container.find_elements(By.XPATH, './/button[contains(@class, "Tya61d")]')
                for button in photo_buttons:
                    style = button.get_attribute("style")
                    # Use regex to extract URL from background-image.
                    m = re.search(r'url\(["\']?(.*?)["\']?\)', style)
                    if m:
                        photos.append(m.group(1))
            except Exception:
                # No photos found for this review.
                pass
            review_data["photos"] = photos

            data["reviews"].append(review_data)
    except Exception as e:
        print(f"Error extracting reviews for {row['Name']}: {e}")

    driver.quit()
    return data


def process_row(row):
    """
    Processes one CSV row:
      - Computes a unique hash from the URL.
      - Checks if the corresponding JSON file exists.
        - If it does, load its data and update the row.
        - Otherwise, scrape the page and save the data.
      - Returns the updated CSV row (with the scraped "ID").
    """
    # Compute a unique hash from the URL.
    row_hash = hashlib.md5(row["URL"].encode("utf-8")).hexdigest()
    json_filename = os.path.join(OUTPUT_FOLDER, f"scrape_{row_hash}.json")
    
    if os.path.exists(json_filename):
        print(f"Skipping already scraped: {row['Name']}")
        try:
            with open(json_filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            row["ID"] = data["id"]
        except Exception as e:
            print(f"Error reading existing JSON for {row['Name']}: {e}")
        return row
    else:
        print(f"Scraping: {row['Name']}")
        data = scrape_place(row, scrape_id=row_hash)
        try:
            with open(json_filename, "w", encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error writing JSON for {row['Name']}: {e}")
        row["ID"] = data["id"]
        return row


def main():
    """
    Main function:
      - Reads the CSV file.
      - Processes each row in parallel:
          - If a row is already scraped (JSON exists), skip scraping.
          - Otherwise, scrape the page.
      - Saves each page’s scraped data into its own JSON file.
      - Writes an updated CSV with a new "ID" column.
    """
    input_csv = "svnsdnt.csv"          # Your input CSV file.
    output_csv = "updated_input_piyushkabir.csv"  # CSV file with an added ID column.

    # Create the output folder if it doesn't exist.
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Read all CSV rows into a list.
    with open(input_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    
    # Process rows concurrently.
    updated_rows = []
    # Adjust max_workers as needed (e.g., os.cpu_count() or a fixed number).
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        # Map process_row across all rows.
        results = list(executor.map(process_row, rows))
        updated_rows.extend(results)
    
    # Write the updated CSV with the new "ID" column.
    if updated_rows:
        fieldnames = list(updated_rows[0].keys())
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
    
    print("Scraping complete. Individual JSON files created (or reused) and updated CSV saved.")


if __name__ == "__main__":
    main()
