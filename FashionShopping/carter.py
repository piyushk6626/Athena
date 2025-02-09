import requests

def fashion_search_api(query="Tshirt For Goa Trip"):        
    

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

    number_of_results=10
    base_url="https://carterapi.onrender.com"
    endpoint = "/search/text/"
    data = {"query": query, "number_of_results": number_of_results}
    
    response = requests.post(f"{base_url}{endpoint}", data=data)
    
    # Check response status
    response.raise_for_status()
    
    dicto={
        "type":"fashion",
        "data" : response.json()
    }
    return dicto




# Example Usage:
if __name__ == "__main__":
    # Text-based search
    
    # Image-based search
    print(fashion_search_api())
    #print(call_search_api(base_url, "/search/image/", query="fashionable summer wear", image_path="path_to_image.jpg", number_of_results=3))