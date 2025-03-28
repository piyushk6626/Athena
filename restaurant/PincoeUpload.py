from pinecone import Pinecone
from openai import OpenAI
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize clients
pc = Pinecone(api_key=PINECONE_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("restaurant_process.log"),
        logging.StreamHandler()
    ]
)

def create_embeddings(content: str) -> list:
    """
    Generate embeddings using the OpenAI API.

    This function takes a content string as input and generates embeddings 
    using the specified OpenAI model. It handles exceptions and logs any 
    errors encountered during the process.

    Args:
        content (str): The input text for which embeddings are to be generated.

    Returns:
        list: A list representing the generated embeddings, or None if an error occurs.
    """
    try:
        # Call the OpenAI API to create embeddings
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=content
        )
        # Return the generated embedding from the response
        return response.data[0].embedding
    except Exception as e:
        # Log any error that occurs during the embedding generation process
        logging.error(f"Error generating embeddings: {e}")
        return None

def read_json_file(file_path: str) -> dict:
    """
    Reads the contents of a JSON file and returns the parsed result.

    This function takes a file path as input and attempts to read the contents
    of the file as JSON. If the file does not contain valid JSON, a JSONDecodeError
    is raised and logged. Any other exceptions encountered are also logged.

    Args:
        file_path (str): The path to the JSON file to read.

    Returns:
        dict: The parsed JSON content of the file, or None if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(
            f"Error decoding JSON from file {file_path}: {e}. "
            "Please verify that the file contains valid JSON."
        )
    except Exception as e:
        logging.error(f"An error occurred while reading file {file_path}: {e}")
    return None

def prepare_content_for_embedding(data: dict) -> str:
    """
    Prepare restaurant content for embedding generation.

    This function takes a restaurant dictionary as input and prepares the content
    that will be used for generating embeddings. The prepared content includes
    the restaurant name, area, rating, tags, reviews, and description. The content
    is formatted as a string, with each field on a separate line.

    Args:
        data: A dictionary containing the restaurant content to be prepared.

    Returns:
        str: The prepared content string, or None if an error occurs.
    """
    try:
        content = f"""
        Restaurant: {data['name']}
        Area: {data['area']}
        Rating: {data['star']} stars from {data['number']} reviews
        Tags: {', '.join(tag['tag'] for tag in data['tags'])}
        Reviews: {' '.join(review['review_text'] for review in data['reviews'])}
        Description: {data['description']}
        """
        return content.strip()
    except Exception as e:
        logging.error(f"An error occurred while preparing content for {data['name']}: {e}")
        return None

def index_restaurant_upsert(
    index: Pinecone.Index, json_file_path: str
) -> None:
    """Upserts a restaurant JSON file's content into the index.

    This function reads a restaurant JSON file, generates embeddings for the
    content if they do not already exist, extracts tags and review texts, and
    upserts the content into the Pinecone index. If the embeddings were generated
    in this call, they are saved back to the file.

    Args:
        index: The Pinecone index to upsert the content into.
        json_file_path: The path to the restaurant JSON file to be upserted.
    """
    data = read_json_file(json_file_path)
    if not data:
        return
    
    try:
        # Check if embeddings need to be generated
        if 'embeddings' not in data or not data['embeddings']:
            logging.info(f"Generating embeddings for {data['name']}")
            content = prepare_content_for_embedding(data)
            embeddings = create_embeddings(content)
            if not embeddings:
                logging.error(f"Failed to generate embeddings for {data['name']}")
                return
        else:
            embeddings = data['embeddings']
        
        # Extract tags into a more searchable format
        tags = {f"tag_{i}": tag['tag'] for i, tag in enumerate(data.get('tags', []))}
        tag_counts = {f"count_{i}": tag['count'] for i, tag in enumerate(data.get('tags', []))}
        
        # Extract review texts
        reviews = [review['review_text'] for review in data.get('reviews', [])]
        
        index.upsert(
            vectors=[
                {
                    "id": data["id"],
                    "values": embeddings,
                    "metadata": {
                        "name": data["name"],
                        "star": data["star"],
                        "number": data["number"],
                        "score": data["score"],
                        "area": data["area"],
                        "url": data["url"],
                        "restaurant_image": data["restaurant_image"],
                        "description": data["description"],
                        "reviews": reviews,
                        **tags,
                        **tag_counts
                    }
                }
            ]
        )
        logging.info(f"Successfully upserted restaurant: {data['name']}")
        
        # If we generated new embeddings, save them back to the file
        if 'embeddings' not in data or not data['embeddings']:
            data['embeddings'] = embeddings
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            logging.info(f"Updated file with new embeddings: {json_file_path}")
            
    except Exception as e:
        logging.error(f"Failed to upsert file {json_file_path}: {e}")

def upload_restaurant_folder(
    index: Pinecone.Index, folder_path: str
) -> None:
    """Uploads all restaurant JSON files from a folder to the index.

    This function loops over all files in the specified folder, checks if they
    are JSON files, and if so, calls index_restaurant_upsert to upsert the
    content from the file into the index.

    Args:
        index (Pinecone.Index): The Pinecone index to upsert the content into.
        folder_path (str): The path to the folder containing the restaurant JSON files.

    Returns:
        None
    """
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            logging.info(f"Processing restaurant file: {filename}")
            index_restaurant_upsert(index, file_path)

if __name__ == "__main__":
    logging.info("Starting Restaurant Data Indexing")
    
    # Initialize the index
    index = pc.Index("restro")
    
    # Example usage:
    upload_restaurant_folder(index, "restaurant_data")