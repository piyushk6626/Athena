from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from .cookies import cook

def scrape_zepto(query):
    
    
    """
    Scrapes Zepto search results for the given query and returns a list of dictionaries containing product details.

    Args:
        query (str): The search query to scrape results for.

    Returns:
        dict: A dictionary with the following structure:
            {
                "type": "zepto",
                "data": [
                    {
                        "url": str,  # URL of the product page
                        "img": str,  # URL of the product image
                        "name": str,  # Name of the product
                        "subtitle": str,  # Subtitle of the product
                        "price": str  # Price of the product
                    },
                    ...
                ]
            }
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (optional)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        url = f"https://www.zeptonow.com/search?query={query}"
        
        driver.get(url)
        
        # Add cookies (Modify as needed)
        for key, value in cook.items():
            driver.add_cookie({'name': key, 'value': value})
        

        driver.get(url)  # Refresh after adding cookies
        
        elements = driver.find_elements(By.XPATH, "//a[@class='!my-0 relative z-0 my-3 rounded-t-xl rounded-b-md group']")
        
        data = []
        for element in elements:
            item = {}
            
            # Extract URL
            try:
                item['url'] = element.get_attribute('href')
            except:
                item['url'] = None
            
            # Extract image source
            try:
                img_element = element.find_element(By.XPATH, ".//div[@class='relative z-0 rounded-xl bg-gray-200']/div[@class='overflow-hidden rounded-xl border-[0.5px] border-gray-200']/img")
                item['img'] = img_element.get_attribute('src')
            except:
                item['img'] = None
                
            # Extract name
            try:
                name_element = element.find_element(By.XPATH, ".//h5[@data-testid='product-card-name']")
                item['name'] = name_element.text
            except:
                item['name'] = None
                
            # Extract subtitle
            try:
                subtitle_element = element.find_element(By.XPATH, ".//h4[@class='font-heading text-lg tracking-wide line-clamp-1 mt-1 !text-sm !font-normal flex items-center']")
                item['subtitle'] = subtitle_element.text
            except:
                item['subtitle'] = None
                
            # Extract price
            try:
                price_element = element.find_element(By.XPATH, ".//h4[@data-testid='product-card-price']")
                item['price'] = price_element.text
            except:
                item['price'] = None
            
            data.append(item)

            if(len(data) == 10):
                break
        # time.sleep(15)
        if data == []:
            final = {
            "type": "text",
            "data": "No Item found."
            }
        else:
             final = {
            "type": "zepto",
            "data": data
            }
        

       
        return final
    finally:
        driver.quit()

# Example usage
# if __name__ == "__main__":
#     query = "Coke diet"  # Replace with the actual search query
#     data = scrape_website(query)
#     print(data)
