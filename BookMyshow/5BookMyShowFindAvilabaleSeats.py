from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def open_url(driver, url):
    driver.get(url)

def random_mouse_movement(driver):
    script = """
    function moveMouseRandomly() {
        let event = new MouseEvent('mousemove', {
            'view': window,
            'bubbles': true,
            'cancelable': true,
            'clientX': Math.floor(Math.random() * window.innerWidth),
            'clientY': Math.floor(Math.random() * window.innerHeight)
        });
        document.dispatchEvent(event);
    }
    moveMouseRandomly();
    """
    driver.execute_script(script)

def click_buy_tickets(driver):
    random_mouse_movement(driver)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='__buytickets']/a"))).click()
    
    random_mouse_movement(driver)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='btnPopupAccept']"))).click()
    
    random_mouse_movement(driver)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//li[@id='pop_3']"))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@id='pop_3']"))).click()

def find_available_seats(driver):
    seat_rows = driver.find_elements(By.XPATH, "//tr/td[@class='SRow1']")
    final_list = []
    
    for row in seat_rows:
        seat_list = []
        seats = row.find_elements(By.XPATH, ".//div[@class='seatI']")
        
        for seat in seats:
            if not seat.find_elements(By.XPATH, "./a"):
                seat_list.append(0)
            elif seat.find_elements(By.XPATH, "./a[@class='_blocked']"):
                seat_list.append(1)
            elif seat.find_elements(By.XPATH, "./a[contains(@class, '_available')]"):
                seat_list.append(2)
        
        final_list.append(seat_list)
    
    return final_list

def main():
    url = "https://in.bookmyshow.com/booktickets/CPFT/20578"
    driver = initialize_driver()
    open_url(driver, url)
    click_buy_tickets(driver)
    time.sleep(5)
    seats = find_available_seats(driver)
    print(seats)
    driver.quit()

if __name__ == "__main__":
    main()
