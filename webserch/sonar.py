from openai import OpenAI
from dotenv import load_dotenv
import os


def serach_the_web_for_news(query:str) -> dict:
    # Load environment variables from .env (e.g., API keys)
    """
    Search the web for news using Perplexity AI Sonar API.

    Args:
        query (str): The query string to search for.

    Returns:
        dict: A dictionary with the following keys:
            - Type (str): The type of response, which is "sonar".
            - response_content (str): The content of the response.
            - response_url (list): A list of URLs cited in the response.

    Raises:
        ValueError: If the query string is empty.
    """
    
    load_dotenv()
    PRELEXITY_API_KEY = os.getenv("PRELEXITY_API_KEY")

    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {   
            "role": "user",
            "content": (
                query
            ),
        },
    ]

    client = OpenAI(api_key=PRELEXITY_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    response_content= response.choices[0].message.content
    response_url=response.citations
    response_dict= {
        "Type":"perplexity",
        "data":{
            "response_content":response_content,
            "response_url":response_url
        }
        
    }
    return response_dict
