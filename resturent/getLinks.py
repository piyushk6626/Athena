import os
import json
import hashlib
import shutil

def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest() + ".json"

def process_json_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    existing_hashes = {f for f in os.listdir(destination_folder)}
    
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        
        if not file_name.endswith(".json"):
            continue
        
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        
        # Ensure required fields exist
        if "url" not in data or "number" not in data or "score" not in data or "reviews" not in data:
            continue

        # Convert "number" and "score" from string to float
        try:
            number = float(data["number"])
            score = float(data["star"])
        except ValueError:
            continue

        # Condition 2: Check if number * score > 2400
        if number * score <= 2400:
            continue

        # Condition 3: Ensure at least one review has non-empty text
        if not any(review.get("review_text", "").strip() for review in data["reviews"]):
            continue

        # Condition 1: Ensure no duplicate URL-based file exists in destination
        new_file_name = hash_url(data["url"])
        if new_file_name in existing_hashes:
            continue

        dest_path = os.path.join(destination_folder, new_file_name)
        shutil.copy(file_path, dest_path)
        existing_hashes.add(new_file_name)

source_folder = "scraped_data"
destination_folder = "scraped_data2"
process_json_files(source_folder, destination_folder)
