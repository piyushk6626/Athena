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