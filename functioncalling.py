from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from tools import TOOLS

client = OpenAI(api_key=OPENAI_API_KEY)

def AGI(messages):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS
    )
    return completion

# A=(completion.choices[0].message.tool_calls)
# print(completion.choices[0].message.content)
# for i in A:
#     print(i)


# print(completion.choices[0].message.content)

#(id='call_nsGrIHxCvxL2qYSLnp4bf9AG', function=Function(arguments='{"location": "Pune, India"}', name='get_weather'), type='function')
# from openai import OpenAI
# client = OpenAI()

 
# response = client.chat.completions.create(
#     model="o1-mini",
    
#     messages=[{"role": "user", "content": "Can you send an email to ilan@example.com and katia@example.com ?"}],
#     tools=tools
# )

# print(response.choices[0].message.content)
# print(response.choices[0].message.content) In order to help you find a movie, could you please provide me with your city and any specific preferences you might have, such as the type of movie you want to watch?

completion=AGI(messages=[
    {
        "role": "user", 
        "content": "i want to wantch a movie tommrow afternoon "
    },
    {
        "role": "assistant", 
        "content": "In order to help you find a movie, could you please provide me with your city and any specific preferences you might have, such as the type of movie you want to watch?"
    },
    {
        "role": "user", 
        "content": "ohk show me for pune "
    },
    {
        "role": "assitant", 
        "content": " "
    }
    ]
               )
A=(completion.choices[0].message.tool_calls)
print(completion.choices[0].message.content)
for i in A:
    print(i)
