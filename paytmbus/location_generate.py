# Uses OpenAI api to get city name

def get_city_name(location):

    import openai
    import os

    openai.api_key = os.getenv("OPENAI_API_KEY")

    city = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"City name for {location}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].text

    return city