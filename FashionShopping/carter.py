import requests

# Configuration settings
API_CONFIG = {
    "base_url": "https://carterapi.onrender.com",
    "default_results": 5
}


def normalize_api_response(data):
    """
    Normalize API response data to ensure consistent string format.
    
    Args:
        data (list): List of dictionaries containing API response items
        
    Returns:
        list: Normalized data with all values converted to strings
    """
    normalized_data = []
    
    for item in data:
        normalized_item = {}
        for key, value in item.items():
            # Handle list values by taking first element
            if isinstance(value, list) and value:
                normalized_item[key] = str(value[0])  
            else:
                # Convert all other values to string
                normalized_item[key] = str(value)  
        normalized_data.append(normalized_item)
    
    return normalized_data


def make_api_request(endpoint, payload):
    """
    Make a POST request to the Carter API.
    
    Args:
        endpoint (str): API endpoint to call
        payload (dict): Data payload for the request
        
    Returns:
        dict: JSON response from the API
        
    Raises:
        requests.exceptions.HTTPError: If the request fails
    """
    # Construct full URL from base and endpoint
    url = f"{API_CONFIG['base_url']}{endpoint}"
    
    # Make POST request with payload
    response = requests.post(url, data=payload)
    
    # Check for HTTP errors
    response.raise_for_status()
    
    return response.json()


def fashion_search_api(query, number_of_results=None):
    """
    Calls the fashion search API with the specified text query.

    Sends a POST request to the Carter API to perform a text-based search
    for fashion items. The API returns a JSON response containing search results.

    Args:
        query (str): The search query for fashion items.
        number_of_results (int, optional): Number of results to return. 
                                          Defaults to API_CONFIG["default_results"].

    Returns:
        dict: A dictionary containing the JSON response from the API, which includes
              the search results.

    Raises:
        requests.exceptions.HTTPError: If the request to the API fails.
    """
    # Use default number of results if not specified
    if number_of_results is None:
        number_of_results = API_CONFIG["default_results"]
        
    # Define API endpoint for text search
    endpoint = "/search/text/"
    
    # Prepare request payload
    payload = {
        "query": query, 
        "number_of_results": number_of_results
    }
    
    # Make API request
    raw_data = make_api_request(endpoint, payload)
    
    # Normalize response data
    normalized_data = normalize_api_response(raw_data)
    
    # Format final response
    response = {
        "type": "fashion",
        "data": normalized_data
    }
    
    return response




# Example Usage:
if __name__ == "__main__":
    # Text-based search example
    print(fashion_search_api("genz cloths"))
    