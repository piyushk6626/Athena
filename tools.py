

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

find_similar_restaurants_tool = {
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
find_products_from_amazon_tool={
    "type": "function",
    "function": {
        "name": "find_products_from_amazon",
        "description": "Find product details from Amazon for a given product keyword.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "product"
            ],
            "properties": {
                "product": {
                    "type": "string",
                    "description": "The product keyword to search for on Amazon."
                }
            },
            "additionalProperties": False
        }
    }
}

send_email_tool={
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email to the given recipient with the given subject and body.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "recipient_email",
                "subject",
                "body"
            ],
            "properties": {
                "recipient_email": {
                    "type": "string",
                    "description": "The email address of the recipient."
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email."
                },
                "body": {
                    "type": "string",
                    "description": "The contents of the email."
                }
            },
            "additionalProperties": False
        }
    }
}

fashion_search_api_tool={
    "type": "function",
    "function": {
        "name": "fashion_search_api",
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
                    "description": "The search query for fashion items. Defaults to 'Tshirt For Goa Trip'."
                }
            },
            "additionalProperties": False
        }
    }
}

find_hotels_tool={
    "type": "function",
    "function": {
        "name": "find_hotels",
        "description": "find hotels data from booking.com.",
        "strict": False,
        "parameters": {
            "type": "object",
            "required": [
                "location",
                "checkin",
                "checkout",
                
            ],
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Location to search for hotels (e.g. 'goa')"
                },
                "checkin": {
                    "type": "string",
                    "description": "Checkin date in the format 'yyyy-mm-dd'"
                },
                "checkout": {
                    "type": "string",
                    "description": "Checkout date in the format 'yyyy-mm-dd'"
                },
                "no_adults": {
                    "type": "number",
                    "description": "Number of adults (default: 1)"
                },
                "no_rooms": {
                    "type": "number",
                    "description": "Number of rooms (default: 1)"
                },
                "no_children": {
                    "type": "number",
                    "description": "Number of children (default: 0)"
                }
            },
            "additionalProperties": False
        }
    }
}

Spotify_action_bot_tool={
    "type": "function",
    "function": {
        "name": "Spotify_action_bot",
        "description": "Process a command into an Spotify Actions object.",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "command"
            ],
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to process."
                }
            },
            "additionalProperties": False
        }
    }
}

get_bus_data_tool = {
    "type": "function",
    "function": {
        "name": "get_bus_data",
        "description": "Returns the scraped data from online bus booking website",
        "strict": True,
        "parameters": {
            "type": "object",
            "required": [
                "source",
                "destination",
                "journey_date"
            ],
            "properties": {
                "source": {
                    "type": "string",
                    "description": "Source city name. The first letter of the city name is capitalized."
                },
                "destination": {
                    "type": "string",
                    "description": "Destination city name. The first letter of the city name is capitalized."
                },
                "journey_date": {
                    "type": "string",
                    "description": "Date of journey in the format YYYY-MM-DD."
                }
            },
            "additionalProperties": False
        }
    }
}

TOOLS=[get_bus_data_tool, Spotify_action_bot_tool,send_email_tool,serach_the_web_for_news_tool,automate_uber_ride,scrape_airbnb_tool,call_fashion_search_api_tool,find_similar_restaurants_tool,scrape_movies_tool,extract_single_movie_show_tool,find_hotels_tool,find_products_from_amazon_tool,fashion_search_api_tool,find_hotels_tool]