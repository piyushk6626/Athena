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