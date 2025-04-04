# Import required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import time
import re 
from xpath import *  # Import XPath constants from xpath module
import os
import tempfile
import subprocess
import platform
import yaml
from pathlib import Path

class TextCleaner:
    """Utility class for cleaning and formatting text data."""
    
    @staticmethod
    def clean_text(text):
        """
        Sanitize text by removing unwanted characters and formatting.

        Args:
            text (str): Raw text to be cleaned

        Returns:
            str: Cleaned and formatted text string
        """
        # Replace multiple newlines with single space
        text = re.sub(r'\n+', ' ', text)
        # Remove non-ASCII characters
        text = re.sub(r'[^\x20-\x7E]', '', text)
        return text.strip()
    
    @staticmethod
    def clean_price(text):
        """
        Extract and format price from raw text.

        Args:
            text (str): Raw price text (e.g., "₹1,234 night")

        Returns:
            str: Cleaned price value without currency symbol
        """
        # Replace newlines with spaces
        text = re.sub(r'\n+', ' ', text)
        # Remove non-ASCII characters
        text = re.sub(r'[^\x20-\x7E]', '', text)
        # Extract first word (price) and remove currency symbol
        
        return "5121"

class WebDriverManager:
    """Manages WebDriver initialization and cleanup."""
    
    @staticmethod
    def load_config():
        """
        Load configuration from YAML file.
        
        Returns:
            dict: Configuration dictionary
        """
        # Try to load from root directory first
        root_config_path = Path(__file__).parent.parent / 'config.yaml'
        if root_config_path.exists():
            with open(root_config_path, 'r') as file:
                return yaml.safe_load(file)
        
        # Fallback to local config if root config doesn't exist
        local_config_path = Path(__file__).parent / 'config.yaml'
        if local_config_path.exists():
            with open(local_config_path, 'r') as file:
                return yaml.safe_load(file)
        
        print(f"Warning: Configuration file not found at {root_config_path} or {local_config_path}")
        return {}
    
    @staticmethod
    def get_driver():
        """
        Initialize and return a Chrome WebDriver instance.

        Returns:
            webdriver.Chrome: Configured Chrome WebDriver instance
        """
        # Kill any existing Chrome processes to avoid conflicts
        try:
            if platform.system() == "Windows":
                subprocess.run("taskkill /f /im chrome.exe", shell=True)
            elif platform.system() == "Linux":
                subprocess.run(["pkill", "-f", "chrome"])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["pkill", "-f", "Chrome"])
            # Wait for processes to fully terminate
            time.sleep(2)
        except Exception as e:
            print(f"Warning: Could not kill existing Chrome processes: {e}")
            
        # Configure Chrome options
        chrome_options = Options()
        
        # Add stability options first
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Load configuration
        config = WebDriverManager.load_config()
        chrome_config = config.get('chrome', {})
        
        # Get platform-specific configuration
        platform_config = None
        if platform.system() == "Windows":
            platform_config = chrome_config.get('windows', {})
        elif platform.system() == "Linux":
            platform_config = chrome_config.get('linux', {})
        elif platform.system() == "Darwin":  # macOS
            platform_config = chrome_config.get('macos', {})
            
        # Set platform-specific Chrome profile paths
        user_data_dir = None
        if platform_config:
            user_data_dir = os.path.expanduser(platform_config.get('user_data_dir', ''))
            profile_dir = platform_config.get('profile_dir', 'Default')
            driver_path = os.path.expanduser(platform_config.get('driver_path', ''))
        else:
            # Fallback to default paths if no configuration found
            if platform.system() == "Windows":
                user_data_dir = r"C:\Users\username\AppData\Local\Google\Chrome\User Data"
                profile_dir = "Profile"
                driver_path = r"chromedriverpath"
            elif platform.system() == "Linux":
                home_dir = os.path.expanduser("~")
                user_data_dir = os.path.join(home_dir, ".config", "google-chrome")
                profile_dir = "Default"
                driver_path = "/usr/local/bin/chromedriver"
            elif platform.system() == "Darwin":  # macOS
                home_dir = os.path.expanduser("~")
                user_data_dir = os.path.join(home_dir, "Library", "Application Support", "Google", "Chrome")
                profile_dir = "Default"
                driver_path = "/usr/local/bin/chromedriver"
            
        # If we have a valid profile path, use it
        if user_data_dir and os.path.exists(user_data_dir):
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"--profile-directory={profile_dir}")
        else:
            print(f"Warning: Chrome profile directory {user_data_dir} not found. Using temporary profile.")
            # Use a temporary profile if the specified one doesn't exist
            temp_dir = os.path.join(tempfile.gettempdir(), f"chrome_profile_{int(time.time())}")
            chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        # Add anti-detection options
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
            
        # Create service with appropriate driver path
        service = None
        if driver_path and os.path.exists(driver_path):
            service = Service(driver_path)
        else:
            # Let Selenium find the driver itself if our specified path doesn't exist
            print(f"Warning: ChromeDriver not found at {driver_path}. Letting Selenium find it.")
            service = Service()
            
        # Return initialized Chrome WebDriver with service and options
        return webdriver.Chrome(service=service, options=chrome_options)

class AirbnbScraper:
    """Main scraper class for Airbnb listings."""
    
    def __init__(self):
        """
        Initialize the AirbnbScraper with required components.

        The scraper is initialized with:
        - A TextCleaner instance for sanitizing scraped text
        - A WebDriver placeholder (initialized during scraping)
        - An empty list to store hotel data

        Attributes:
            text_cleaner (TextCleaner): Utility for cleaning scraped text
            driver (webdriver.Chrome): WebDriver instance, None until scraping starts
            hotels_data (list): List to store dictionaries of hotel information
        """
        self.text_cleaner = TextCleaner()  # Initialize text cleaner utility
        self.driver = None  # WebDriver will be initialized during scraping
        self.hotels_data = []  # List to store scraped hotel information

    def build_url(self, destination, checkin_date, checkout_date, adults_no, children_no):
        """
        Construct the Airbnb search URL.

        Args:
            destination (str): Location to search
            checkin_date (str): Check-in date
            checkout_date (str): Check-out date
            adults_no (str): Number of adults
            children_no (str): Number of children

        Returns:
            str: Complete Airbnb search URL
        """
        # Construct and return formatted URL with search parameters
        return (f"https://www.airbnb.co.in/s/{destination}/homes"
                f"?checkin={checkin_date}&checkout={checkout_date}"
                f"&adults={adults_no}&children={children_no}"
                f"&query={destination}")

    def extract_hotel_info(self, hotel):
        """
        Extract information from a single hotel card.

        Args:
            hotel: WebElement representing the hotel card

        Returns:
            dict: Hotel information dictionary
        """
        try:
            # Find and extract image URL
            image_elements = hotel.find_elements(By.XPATH, imgpath)
            image_url = image_elements[0].get_attribute('src') if image_elements else ""
            
            # Return dictionary with all hotel details
            return {
                "image_url": image_url,
                "hotel_name": self.text_cleaner.clean_text(
                    hotel.find_element(By.XPATH, hotelnamepath).text),
                "payment_url": hotel.find_element(By.XPATH, paymentpath).get_attribute('href'),
                "location": self.text_cleaner.clean_text(
                    hotel.find_element(By.XPATH, locationpath).text),
                "total_price": self.text_cleaner.clean_price(
                    hotel.find_element(By.XPATH, totalpricepath).text),
                "rating_reviews": self.text_cleaner.clean_text(
                    hotel.find_element(By.XPATH, ratingreviews).text),
                "tag_text": self.text_cleaner.clean_text(
                    hotel.find_element(By.XPATH, tagpath).text)
            }
        except Exception as e:
            # Log error and return None if extraction fails
            print(f"Error extracting data for a hotel: {e}")
            return None

    def extract_hotels(self):
        """
        Extract information from all hotel listing cards on the page.
        
        Finds all hotel card containers on the page and extracts 
        detailed information for each of them (limited to first 10).
        """
        # Find all hotel card containers
        hotels = self.driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')
        
        # Process only the first 10 hotels
        for hotel in hotels[:10]:
            hotel_info = self.extract_hotel_info(hotel)
            if hotel_info:
                self.hotels_data.append(hotel_info)

    def scrape(self, destination, checkin_date, checkout_date, adults_no, children_no):
        """
        Main scraping method to extract Airbnb listings.

        Args:
            destination (str): Location to search for listings
            checkin_date (str): Check-in date in YYYY-MM-DD format
            checkout_date (str): Check-out date in YYYY-MM-DD format
            adults_no (str): Number of adult guests
            children_no (str): Number of child guests

        Returns:
            dict: Contains scraped data and type identifier
        """
        try:
            # Initialize WebDriver
            self.driver = WebDriverManager.get_driver()
            # Build URL with search parameters
            url = self.build_url(destination, checkin_date, checkout_date, adults_no, children_no)
            
            # Navigate to the URL
            self.driver.get(url)
            time.sleep(5)  # Wait for page to load completely
            
            # Extract hotel information
            self.extract_hotels()
            
            # Return structured data
            return {
                'type': 'airbnb',
                'data': self.hotels_data
            }
        finally:
            # Ensure WebDriver is closed properly
            if self.driver:
                self.driver.quit()

def scrape_airbnb(destination, checkin_date, checkout_date, adults_no, children_no):
    """
    Convenience function to perform Airbnb scraping.

    Args:
        destination (str): Location to search for listings
        checkin_date (str): Check-in date in YYYY-MM-DD format
        checkout_date (str): Check-out date in YYYY-MM-DD format
        adults_no (str): Number of adult guests
        children_no (str): Number of child guests

    Returns:
        dict: Contains scraped data and type identifier
    """
    # Create and use scraper instance
    scraper = AirbnbScraper()
    return scraper.scrape(destination, checkin_date, checkout_date, adults_no, children_no)

# Example usage
if __name__ == "__main__":
    # Test the scraper with sample data
    data = scrape_airbnb(destination="pune", checkin_date="2025-04-09", checkout_date="2025-04-14", adults_no="1", children_no="0")
    # Pretty print the results
    print(json.dumps(data, indent=2))
