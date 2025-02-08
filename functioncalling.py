from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from tools import TOOLS

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
},{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}
         ]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Send email to abc@example.com about movies available in pune"}],
    tools=TOOLS
)

A=(completion.choices[0].message.tool_calls)

for i in A:
    print(i)


print(completion.choices[0].message.content)

#(id='call_nsGrIHxCvxL2qYSLnp4bf9AG', function=Function(arguments='{"location": "Pune, India"}', name='get_weather'), type='function')
# from openai import OpenAI
# client = OpenAI()

 
# response = client.chat.completions.create(
#     model="o1-mini",
    
#     messages=[{"role": "user", "content": "Can you send an email to ilan@example.com and katia@example.com ?"}],
#     tools=tools
# )

# print(response.choices[0].message.content)
# print(response.choices[0].message.content)