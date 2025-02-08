from pinecone import Pinecone
from openai import OpenAI
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
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

def create_embeddings(content):
    """Generate embeddings using OpenAI API."""
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=content
        )
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        return None

def read_json_file(file_path):
    """Reads a JSON file and returns its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from file {file_path}: {e}")
    except Exception as e:
        logging.error(f"An error occurred while reading file {file_path}: {e}")
    return None

def prepare_content_for_embedding(data):
    """Prepare restaurant content for embedding generation."""
    content = f"""
    Restaurant: {data['name']}
    Area: {data['area']}
    Rating: {data['star']} stars from {data['number']} reviews
    Tags: {', '.join(tag['tag'] for tag in data['tags'])}
    Reviews: {' '.join(review['review_text'] for review in data['reviews'])}
    Description: {data['description']}
    """
    return content.strip()

def index_restaurant_upsert(index, json_file_path):
    """Upserts a restaurant JSON file's content into the index."""
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

def upload_restaurant_folder(index, folder_path):
    """Uploads all restaurant JSON files from a folder to the index."""
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            logging.info(f"Processing restaurant file: {filename}")
            index_restaurant_upsert(index, file_path)

if __name__ == "__main__":
    logging.info("Starting Restaurant Data Indexing")
    
    # Initialize the index
    index = pc.Index("bits")
    
    # Example usage:
    upload_restaurant_folder(index, "restaurant_data")