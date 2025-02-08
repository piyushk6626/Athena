from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

tools = [{
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email to a given recipient with a subject and message.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "The recipient email address."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line."
                },
                "body": {
                    "type": "string",
                    "description": "Body of the email message."
                }
            },
            "required": [
                "to",
                "subject",
                "body"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Can you send an email to ilan@example.com and katia@example.com sa?"}],
    tools=tools
)

print(completion.choices[0].message.tool_calls)
print(completion.choices[0].message.content)

# from openai import OpenAI
# client = OpenAI()


# response = client.chat.completions.create(
#     model="o1-mini",
    
#     messages=[{"role": "user", "content": "Can you send an email to ilan@example.com and katia@example.com ?"}],
#     tools=tools
# )

# print(response.choices[0].message.content)
# print(response.choices[0].message.content)