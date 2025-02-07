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
    """
    Query the index and return the top k results that match the query vector.

    Parameters
    ----------
    index: pinecone.Index
        The Pinecone index to query
    query_vector: list
        The vector to query the index with
    number_of_results: int
        The number of results to return

    Returns
    -------
    results: list
        The top k results that match the query vector, along with their metadata
    """
    # Query the index with the query vector and return the top k results
    results = index.query_namespaces(
        vector=query_vector,
        namespaces=[""],  # Search in the default namespace
        metric="cosine",  # Use cosine similarity as the metric
        top_k=number_of_results,  # Return the top k results
        include_values=False,  # Don't include the actual vectors in the results
        include_metadata=True,  # Include the metadata in the results
        show_progress=False,  # Don't show the progress bar
    )

    # Return the results
    return results

def find_similar_items(query: str, number_of_results: int = 5) -> list:
    """
    Find items in the Pinecone index that are similar to the given query string.

    This function takes a query string, converts it into embeddings, and queries the Pinecone index
    to find and return a list of items that are similar to it. The similarity is measured using the
    cosine similarity metric.

    Parameters
    ----------
    query: str
        The query string for which similar items are to be found.
    number_of_results: int, optional
        The number of similar items to return. Defaults to 30.

    Returns
    -------
    results: list
        A list of items similar to the query string, including their metadata.
    """
    # Get the Pinecone index using a helper function
    index = get_index()

    # Generate vector embeddings for the query string
    vector = create_embeddings(query)

    # Query the Pinecone index with the generated embeddings
    results = query_index(index, vector, number_of_results)

    # Return the list of results
    return results


if __name__ == "__main__":
    Output=find_similar_items("kokni food with grate ambiance")

    print(Output)