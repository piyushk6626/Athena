from openai import OpenAI
from dotenv import load_dotenv
import os


def serach_the_web_for_news(qury:str) -> dict:
    # Load environment variables from .env (e.g., API keys)
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
                qury
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
        "Type":"sonar",
        "response_content":response_content,
        "response_url":response_url
    }
    return response_dict

r=serach_the_web_for_news("Donald Trump  athleate ban")

print(r)