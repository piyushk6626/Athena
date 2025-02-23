from pinecone import Pinecone
from openai import OpenAI
import json
import os
import logging
from dotenv import load_dotenv


def normalize_restaurant_data(result):
    # If the result object has a 'matches' attribute, use it
    if hasattr(result, 'matches'):
        data = result.matches
    # Alternatively, if it's a dict with a "matches" key, use that
    elif isinstance(result, dict) and "matches" in result:
        data = result["matches"]
    else:
        data = result  # Assume result is already a list

    normalized_data = []
    for item in data:
        metadata = item.get("metadata", {})
        tagslist=[str(metadata[key]) for key in metadata if key.startswith("tag_")]
        result = ", ".join(tagslist)
    
        normalized_item = {
            "name": str(metadata.get("name", "")),
            "star": str(metadata.get("star", "")),
            "number_of_reviews": str(metadata.get("number", "")),
            "image": str(metadata.get("restaurant_image", "")),
            "url": str(metadata.get("url", "")),
            "tags":result
        }
        normalized_data.append(normalized_item)

    return normalized_data
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


# Set up Pinecone API
def get_index():
    """
    Load environment variables, initialize the Pinecone client, and return the index.
    """
    # Load environment variables from a .env file
    load_dotenv()

    # Retrieve Pinecone API key and host URL from environment variables
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_host = os.getenv("PINECONE_HOST_URL")

    # Initialize the Pinecone client with the API key
    pc = Pinecone(api_key=pinecone_api_key)

    # Create and return the index using the host URL
    index = pc.Index(host=pinecone_host)
    return index


def query_index(index, query_vector, number_of_results):
    # Query the index
    response = index.query_namespaces(
        vector=query_vector,
        namespaces=[""],        # Search in the default namespace
        metric="cosine",        # Use cosine similarity
        top_k=number_of_results,
        include_values=False,
        include_metadata=True,
        show_progress=False,
    )

    # Assume the response is a dict or object with a 'matches' key/attribute
    if hasattr(response, 'matches'):
        return response.matches
    elif isinstance(response, dict) and "matches" in response:
        return response["matches"]
    else:
        return response

def find_similar_items(query: str) -> list:
   
    """
    Find similar items based on a query string using Pinecone.

    This function takes a query string, generates vector embeddings for it,
    and queries a Pinecone index to find and return the top similar items.

    Args:
        query (str): The query string to find similar items for.

    Returns:
        list: A list of results that are most similar to the query string.
    """

    number_of_results: int = 5
    # Get the Pinecone index using a helper function
    index = get_index()

    #update the query based on given format 
    explained_query=explain_UserQuery(query)

    # Generate vector embeddings for the query string
    vector = create_embeddings(explained_query)

    # Query the Pinecone index with the generated embeddings
    results = query_index(index, vector, number_of_results)

    # Return the list of results
    data= normalize_restaurant_data(results)
    dicto={
        "type": "restaurant",
        "data": data
    }
    return dicto

SystemPrompt="""Write a concise description to help the user find a restaurant based on their query and the following points:

1. **Ambiance & Design**:
   - Décor, lighting, and standout features from photos.
   - Music or atmosphere insights from reviews.

2. **Menu & Culinary Experience**:
   - Signature dishes and specialties.
   - Food presentation and dietary options if available.

3. **Customer Experience & Service**:
   - Staff friendliness and service efficiency.
   - Information on reservation or walk-in policies.

4. **Pricing**:
   - Consider user preferences for cost. 
"""

def explain_UserQuery(query: str) -> str :
    messages=[
            {"role": "system", "content": SystemPrompt},
            {"role": "user", "content": query}
        ]
    
    Explained_Qury=client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        temperature=0.9
        
    )
        
        
    
    return Explained_Qury.choices[0].message.content
    
    
    
    

if __name__ == "__main__":
    Output=find_similar_items("Kokani food near me")

    print(Output)