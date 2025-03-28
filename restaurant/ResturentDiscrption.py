import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from dotenv import load_dotenv
from .prompts import SystemPrompt
# Load environment variables from .env (e.g., API keys)
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(f"API Key: {OPENAI_API_KEY}")
client = OpenAI(api_key=OPENAI_API_KEY)


# The folder containing the JSON files
data_folder = "restaurant_data"  # Ensure this folder exists and contains your JSON files

def emmbedings(content):
    """
    Generate embeddings for the given content using the OpenAI API.

    This function takes a content string as input and generates embeddings 
    using a specified OpenAI model. It returns the generated embeddings 
    from the response.

    Args:
        content (str): The input text for which embeddings are to be generated.

    Returns:
        list: A list representing the generated embeddings.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=content
    )
    return response.data[0].embedding

def process_file(filename):
    """
    Process a single JSON file containing restaurant data.

    :param filename: The name of the JSON file to process.
    :return: None
    """
    
    file_path = os.path.join(data_folder, filename)
    
    # Load the JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Skip if the file already contains a description
    if data.get("description"):
        print(f"Skipping {filename} as it already has a description.")
        return

    # Extract fields from the JSON data
    name = data.get("name", "Unknown")
    area = data.get("area", "Unknown")
    star = data.get("star", "N/A")
    number = data.get("number", "N/A")
    tags_list = data.get("tags", [])
    # Format tags as "tag (count)" pairs
    tags_formatted = ", ".join([f'{tag["tag"]} ({tag["count"]})' for tag in tags_list])

    # Process reviews: use up to the first three reviews
    reviews = data.get("reviews", [])
    review_texts = []
    image_urls = []
    for review in reviews[:3]:
        review_texts.append(review.get("review_text", ""))
        photos = review.get("photos", [])
        # Take roughly half of the images per review. For instance, if there are 4 photos, take the first 2.
        if photos:
            half = len(photos) // 2 if len(photos) > 1 else 1
            image_urls.extend(photos[:half])
    # Ensure we only have at most 6 images total
    image_urls = image_urls[:6]

    # Prepare the input string using the specified format
    user_input = (
        f"NAME OF THE RESTAURANT IS {name} LOCATED IN {area} RATING IS {star} AND NUMBER OF PPL WHO RATED IT IS {number}\n"
        f"THESE ARE FOLLOWING TAGS WITH THIER FREQUENCY COUNT {tags_formatted}\n"
        f"FOLLOWING ARE REVIEWS REVIEW 1 : {review_texts[0] if len(review_texts) > 0 else 'N/A'}, "
        f"REVIEW 2 : {review_texts[1] if len(review_texts) > 1 else 'N/A'}, "
        f"REVIEW 3 : {review_texts[2] if len(review_texts) > 2 else 'N/A'}\n"
        f"AND THE IMAGE URLS ARE: {', '.join(image_urls)}"
    )

    # Prepare the message list for the OpenAI chat completion call
    messages = [
        {"role": "system", "content": SystemPrompt},
        {"role": "user", "content": user_input}
    ]

    try:
        # Call the OpenAI chat completion endpoint
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Adjust the model name if necessary
            messages=messages,
        )

        # Retrieve the generated narrative description for the current restaurant
        narrative = response.choices[0].message.content

        # Update the data with the narrative and its embeddings
        data["description"] = narrative
        data["embeddings"] = emmbedings(narrative)

        # Save the updated data back to the JSON file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Print usage details and confirmation
        print(f"{filename}: Input tokens: {response.usage.prompt_tokens}, Output tokens: {response.usage.completion_tokens}")
        print(f"Updated '{filename}' with generated description.")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

def main():
    # List all JSON files in the data folder
    files = [filename for filename in os.listdir(data_folder) if filename.endswith('.json')]

    # Use ThreadPoolExecutor to process files concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Create a future for each file
        futures = {executor.submit(process_file, filename): filename for filename in files}

        # Optionally, wait for all futures to complete and handle exceptions
        for future in as_completed(futures):
            filename = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f"{filename} generated an exception: {exc}")

if __name__ == '__main__':
    main()
