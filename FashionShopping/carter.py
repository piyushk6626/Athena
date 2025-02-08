import requests

def call_fashion_search_api(query="Tshirt For Goa Trip", number_of_results=10):        
    """
    Call the fashion search API with a query and number of results to return.

    Args:
        query (str): The search query to send to the API. Defaults to "Tshirt For Goa Trip".
        number_of_results (int): The number of results to retrieve. Defaults to 10.

    Returns:
        dict: The JSON response from the API, containing the results of the search.

    Raises:
        requests.exceptions.HTTPError: If the API returns an unsuccessful status code.
    """
    base_url="https://carterapi.onrender.com"
    endpoint = "/search/text/"
    data = {"query": query, "number_of_results": number_of_results}
    
    response = requests.post(f"{base_url}{endpoint}", data=data)
    
    # Check response status
    response.raise_for_status()
    return response.json()




# Example Usage:
if __name__ == "__main__":
    base_url = "http://localhost:8000"  # Replace with your FastAPI server's base URL
    # Text-based search
    
    # Image-based search
    #print(call_search_api(base_url, "/search/image/", query="fashionable summer wear", image_path="path_to_image.jpg", number_of_results=3))