from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json
import time

def scroll_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_position = 0
    
    while True:
        current_position += 1000
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if current_position >= new_height:
            break
        last_height = new_height

def get_product_details(container):
    try:
        title=""
        try:
            container.find_element(By.CSS_SELECTOR, 'h2.a-size-medium')
            title=container.find_element(By.CSS_SELECTOR, 'h2.a-size-medium').text 
        except:
            title=container.find_element(By.CSS_SELECTOR, 'h2.a-size-base-plus').text

        
        amazonchoice=container.find_element(By.CSS_SELECTOR, 'span.a-badge-label-inner .a-badge-text').text if container.find_elements(By.CSS_SELECTOR, 'span.a-badge-label-inner') else None
        if amazonchoice:
            amazonchoice=str(amazonchoice)
        else:
            amazonchoice=False
        product_data = {
            'title': title ,
            'price': str(container.find_element(By.CSS_SELECTOR, 'span.a-price').text),
            'rating': str(container.find_element(By.CSS_SELECTOR, 'i.a-icon-star-small span.a-icon-alt').get_attribute('innerHTML')),
            'review_count': str(container.find_element(By.CSS_SELECTOR, 'a[aria-label*="ratings"] span.a-size-base').text),
            'amazons_choice': amazonchoice,
            'image_url': str(container.find_element(By.CSS_SELECTOR, 'img.s-image').get_attribute('src')),
            'product_url': str(container.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-link-style').get_attribute('href')),
            'number of buyers': str(container.find_element(By.XPATH, '//div[contains(@class, "puis-card-container s-card-container")]//div[@class="a-section a-spacing-none a-spacing-top-micro"]//span[contains(@class, "a-size-base a-color-secondary")]').text)
        }
        
        return {"type":"Amazon","data":product_data}
        
    
    except NoSuchElementException as e:
        print(f"Missing element: {str(e)}")
        return None

def scrape_products_from_amazon(product:str)->list[dict]:
    """
    Scrapes product details from Amazon for a given product keyword.

    This function uses a Selenium WebDriver to navigate to Amazon's search results
    page for the specified product keyword. It scrolls through the page to load
    all the product containers and extracts details such as title, price, rating,
    review count, Amazon's choice badge, image URL, product URL, and the number of
    buyers for each product.

    Args:
        product (str): The product keyword to search for on Amazon.

    Returns:
        list[dict]: A list of dictionaries, each containing product details. If an
        error occurs or no products are found, an empty list is returned.
    """

    url = "https://www.amazon.com/s?k="+product
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    products_data = []
    
    try:

        driver.get("https://www.amazon.com/")
        driver.get(url)

        scroll_page(driver)
        
        wait = WebDriverWait(driver, 20)
        containers = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'span.a-declarative')
        ))
        
        print(f"Found {len(containers)} product containers")
        
        for container in containers:
            product_data = get_product_details(container)
            if product_data:
                products_data.append(product_data)
            
        
        return products_data
    
    except TimeoutException:
        print("Timeout while waiting for elements to load")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    finally:
        driver.quit()

if __name__ == "__main__":
    product = "laptop"
    products = scrape_products_from_amazon(product)
    print(products)
    # with open('products_data.json', 'w', encoding='utf-8') as f:
    #     json.dump(products, f, ensure_ascii=False, indent=4)
    # print(f"Scraped {len(products)} products successfully!")
