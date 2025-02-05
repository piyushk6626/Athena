import os
import json
import hashlib

def rename_files_to_hash(folder_path):
    """
    Iterates over JSON files in folder_path, reads their 'url' field, computes an MD5 hash,
    and renames the file to 'scrape_<hash>.json'.
    
    Parameters:
      folder_path (str): The directory where your JSON files are stored.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            url = data.get("url")
            if not url:
                print(f"File {filename} does not have a 'url' field. Skipping.")
                continue

            # Compute the MD5 hash of the URL.
            file_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
            new_filename = f"scrape_{file_hash}.json"
            new_file_path = os.path.join(folder_path, new_filename)

            # Check if the file is already correctly named.
            if os.path.abspath(file_path) == os.path.abspath(new_file_path):
                print(f"{filename} is already correctly named.")
            else:
                if os.path.exists(new_file_path):
                    print(f"A file named {new_filename} already exists. Skipping {filename}.")
                else:
                    try:
                        print(f"Renaming {filename} to {new_filename}")
                        os.rename(file_path, new_file_path)
                    except Exception as e:
                        print(f"Error renaming {filename}: {e}")

if __name__ == "__main__":
    # Specify the folder that contains your existing JSON files.
    folder = "scraped_data4"
    if not os.path.exists(folder):
        print(f"Folder '{folder}' does not exist.")
    else:
        rename_files_to_hash(folder)
