from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configure Chrome options to mimic a regular user browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("start-maximized")
# Remove automation flags (this may help reduce detection)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# Optionally use your regular user profile to avoid “not secure” errors:
# chrome_options.add_argument("user-data-dir=/path/to/your/chrome/profile")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

# Step 1. Go to Uber’s login page that offers "Sign in with Google"
driver.get("https://auth.uber.com/login/")  # Adjust the URL if needed

# Step 2. Locate and click the “Continue with Google” button.
# (You may need to inspect the Uber login page to update the selector below.)
google_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue with Google')]")))
google_btn.click()

# If Google’s login page opens in a new window, switch to it:
time.sleep(2)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])

# Step 3. On the Google login page, enter your Gmail address
email_field = wait.until(EC.visibility_of_element_located((By.ID, "identifierId")))
email_field.send_keys("112315132@cse.iiitp.ac.in")
driver.find_element(By.ID, "identifierNext").click()
time.sleep(2)

# Step 4. Wait for the password field and enter your password
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])
    
driver.find_element(By.XPATH, "(//input)[2]").click()
password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@class='whsOnd zHQkBf']")))
time.sleep(1)  # slight pause can help stability
password_field.send_keys("Maa_3696")
driver.find_element(By.XPATH, "(//button)[2]").click()

time.sleep(10)

# Step 5.Switch back to the original window if needed:
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[0])

print("Login process completed.")
