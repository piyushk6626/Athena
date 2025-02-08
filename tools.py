A={
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

serach_the_web_for_news_tool={
    "type": "function",
    "function": {
        "name": "serach_the_web_for_news",
        "description": "Search the web for letest news And return summerized answer using LLM .",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query user Send to Find Letest news about it"
                }
                
            },
            "required": [
                "query"
                
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}

automate_uber_ride={
    "type": "function",
    "function": {
        "name": "automate_uber_ride",
        "description": "Automates the process of booking an Uber ride using a web browser.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "pickup_location",
                "destination"
            ],
            "properties": {
                "pickup_location": {
                    "type": "string",
                    "description": "The address or name of the pickup location."
                },
                "destination": {
                    "type": "string",
                    "description": "The address or name of the destination."
                }
            },
            "additionalProperties": False
        }
    }
}

scrape_airbnb_tool={
    "type": "function",
    "function": {
        "name": "scrape_airbnb",
        "description": "Scrape Airbnb for hotels based on destination, check-in date, check-out date, number of adults, and number of children.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "destination",
                "checkinDate",
                "checkoutDate",
                "adultsNo",
                "childrenNo"
            ],
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "Destination for searching hotels."
                },
                "checkinDate": {
                    "type": "string",
                    "description": "Check-in date for booking."
                },
                "checkoutDate": {
                    "type": "string",
                    "description": "Check-out date for booking."
                },
                "adultsNo": {
                    "type": "string",
                    "description": "Number of adults."
                },
                "childrenNo": {
                    "type": "string",
                    "description": "Number of children."
                }
            },
            "additionalProperties": False
        }
    }
}


call_fashion_search_api_tool = {
    "type": "function",
    "function": {
        "name": "call_fashion_search_api",
        "description": "Calls the fashion search API with the specified text query.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "query"
            ],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for fashion items."
                }
            },
            "additionalProperties": False
        }
    }
}

find_similar_items_tool = {
    "type": "function",
    "function": {
        "name": "find_similar_restaurants",
        "description": "Find similar restaurants based on a query string.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "query"
            ],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query string to find similar restaurants for."
                }
            },
            "additionalProperties": False
        }
    }
}

scrape_movies_tool = {
    "type": "function",
    "function": {
        "name": "scrape_movies",
        "description": "Scrapes the list of movies available in the given city. Returns a JSON string with movie details.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "city"
            ],
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city for which to scrape available movies"
                }
            },
            "additionalProperties": False
        }
    }
}


extract_single_movie_show_tool = {
    "type": "function",
    "function": {
        "name": "extract_single_movie_show",
        "description": "Extracts movie show details from the Paytm page after selecting the specified city and language. Returns a list of dictionaries containing the show details.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "url",
                "city",
                "language"
            ],
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the Paytm page to extract movie shows from"
                },
                "city": {
                    "type": "string",
                    "description": "The city for which to fetch the movie shows"
                },
                "language": {
                    "type": "string",
                    "description": "The language preference for the movie shows"
                }
            },
            "additionalProperties": False
        }
    }
}