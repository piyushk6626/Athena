import requests


def normalize_api_response(data):
    normalized_data = []
    
    for item in data:
        normalized_item = {}
        for key, value in item.items():
            if isinstance(value, list) and value:
                normalized_item[key] = str(value[0])  # Pick first element and convert to string
            else:
                normalized_item[key] = str(value)  # Convert directly to string
        normalized_data.append(normalized_item)
    
    return normalized_data



def fashion_search_api(query):        
    

    """
    Calls the fashion search API with the specified text query.

    Sends a POST request to the Carter API to perform a text-based search
    for fashion items. The API returns a JSON response containing search results.

    Args:
        query (str): The search query for fashion items. Defaults to "Tshirt For Goa Trip".

    Returns:
        dict: A dictionary containing the JSON response from the API, which includes
              the search results.

    Raises:
        requests.exceptions.HTTPError: If the request to the API fails.
    """

    number_of_results=5
    base_url="https://carterapi.onrender.com"
    endpoint = "/search/text/"
    data = {"query": query, "number_of_results": number_of_results}
    
    response = requests.post(f"{base_url}{endpoint}", data=data)
    
    # Check response status
    response.raise_for_status()
    data=normalize_api_response(response.json())
    dicto={
        "type":"fashion",
        "data" : data
    }
    return dicto




# Example Usage:
if __name__ == "__main__":
    # Text-based search
    
    # Image-based search
    print(fashion_search_api("genz cloths"))
    #print(call_search_api(base_url, "/search/image/", query="fashionable summer wear", image_path="path_to_image.jpg", number_of_results=3))