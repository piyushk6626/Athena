"""
Semantic Search Module for Restaurant Data

This module provides functionality for searching restaurants using natural language queries.
It leverages OpenAI's GPT models for query understanding and Pinecone's vector database
for efficient similarity search. The module handles:
- Query processing and embedding generation
- Vector similarity search
- Result normalization and formatting
- Error handling and logging
"""

from pinecone import Pinecone
from openai import OpenAI
from .prompts import SystemPromptSearch
import os
import logging
from dotenv import load_dotenv

# Configure logging for better debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("restaurant_process.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables and initialize clients
load_dotenv(override=True)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize API clients
pc = Pinecone(api_key=PINECONE_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def normalize_restaurant_data(result):
    """
    Normalize and format restaurant search results for consistent output.
    
    This function processes the raw search results from Pinecone and formats them
    into a standardized structure. It handles different result formats and extracts
    relevant metadata including tags, ratings, and images.
    
    Args:
        result: Raw search results from Pinecone, which can be:
            - An object with a 'matches' attribute
            - A dictionary with a "matches" key
            - A direct list of matches
            
    Returns:
        list: List of normalized restaurant dictionaries containing:
            - name: Restaurant name
            - star: Rating
            - number_of_reviews: Total review count
            - image: Restaurant image URL
            - url: Google Maps URL
            - tags: Comma-separated list of tags
    """
    # Handle different result formats
    if hasattr(result, 'matches'):
        data = result.matches
    elif isinstance(result, dict) and "matches" in result:
        data = result["matches"]
    else:
        data = result

    normalized_data = []
    for item in data:
        metadata = item.get("metadata", {})
        # Extract all tags from metadata
        tagslist = [str(metadata[key]) for key in metadata if key.startswith("tag_")]
        result = ", ".join(tagslist)
    
        # Create normalized restaurant entry
        normalized_item = {
            "name": str(metadata.get("name", "")),
            "star": str(metadata.get("star", "")),
            "number_of_reviews": str(metadata.get("number", "")),
            "image": str(metadata.get("restaurant_image", "")),
            "url": str(metadata.get("url", "")),
            "tags": result
        }
        normalized_data.append(normalized_item)

    return normalized_data

def create_embeddings(content):
    """
    Generate embeddings for text content using OpenAI's API.
    
    This function takes text content and converts it into vector embeddings
    using OpenAI's text-embedding-3-large model. The embeddings are used for
    semantic similarity search in the Pinecone vector database.
    
    Args:
        content (str): The text content to generate embeddings for
        
    Returns:
        list: Vector embeddings for the input content, or None if an error occurs
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-large",
            input=content
        )
        return response.data[0].embedding
    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
        return None

def get_index():
    """
    Initialize and return a Pinecone index for vector search.
    
    This function loads environment variables and creates a connection to the
    Pinecone vector database. It handles the initialization of the Pinecone
    client and index creation.
    
    Returns:
        Pinecone.Index: Initialized Pinecone index for vector search operations
    """
    # Load environment variables
    load_dotenv()

    # Get Pinecone configuration from environment
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_host = os.getenv("PINECONE_HOST_URL")

    # Initialize Pinecone client and create index
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(host=pinecone_host)
    return index

def query_index(index, query_vector, number_of_results):
    """
    Query the Pinecone index for similar vectors.
    
    This function performs a similarity search in the Pinecone vector database
    using the provided query vector. It searches in the default namespace and
    returns the top-k most similar results.
    
    Args:
        index (Pinecone.Index): The Pinecone index to query
        query_vector (list): The vector to search for
        number_of_results (int): Number of results to return
        
    Returns:
        list: List of matches from the vector search
    """
    # Perform vector similarity search
    response = index.query_namespaces(
        vector=query_vector,
        namespaces=[""],        # Search in default namespace
        metric="cosine",        # Use cosine similarity
        top_k=number_of_results,
        include_values=False,
        include_metadata=True,
        show_progress=False,
    )

    # Handle different response formats
    if hasattr(response, 'matches'):
        return response.matches
    elif isinstance(response, dict) and "matches" in response:
        return response["matches"]
    else:
        return response

def explain_UserQuery(query: str) -> str:
    """
    Process and enhance user queries using GPT model.
    
    This function takes a natural language query and uses GPT to generate
    a more detailed and structured version that better captures the user's
    intent for restaurant search.
    
    Args:
        query (str): The original user query
        
    Returns:
        str: Enhanced query with additional context and structure
    """
    # Prepare messages for GPT model
    messages = [
        {"role": "system", "content": SystemPromptSearch},
        {"role": "user", "content": query}
    ]
    
    # Generate enhanced query using GPT
    Explained_Qury = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        temperature=0.9
    )
    
    return Explained_Qury.choices[0].message.content

def find_similar_items(query: str) -> dict:
    """
    Find restaurants similar to the given query using semantic search.
    
    This function implements the complete search pipeline:
    1. Enhances the user query using GPT
    2. Generates embeddings for the enhanced query
    3. Performs vector similarity search
    4. Normalizes and formats the results
    
    Args:
        query (str): Natural language query describing desired restaurants
        
    Returns:
        dict: Dictionary containing:
            - type: Always "restaurant"
            - data: List of matching restaurants with their details
    """
    number_of_results: int = 5
    # Get Pinecone index
    index = get_index()

    # Enhance query using GPT
    explained_query = explain_UserQuery(query)

    # Generate embeddings for search
    vector = create_embeddings(explained_query)

    # Perform vector similarity search
    results = query_index(index, vector, number_of_results)

    # Normalize and format results
    data = normalize_restaurant_data(results)
    
    # Return formatted response
    return {
        "type": "restaurant",
        "data": data
    }

if __name__ == "__main__":
    # Example usage
    Output = find_similar_items("Kokani food in pune")
    print(Output)