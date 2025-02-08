scrape_products_from_amazon_tool={
    "type": "function",
    "function": {
        "name": "scrape_products_from_amazon",
        "description": "Scrapes product details from Amazon for a given product keyword.",
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

{
    "type": "function",
    "function": {
        "name": "scrape_hotels",
        "description": "Scrape hotel data from booking.com.",
        "strict": True,
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