import pytest
import time
from selenium import webdriver
from bs4 import BeautifulSoup
# Wait for the div to be generated 
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 

import requests
import os

start_date = "2024-04-15"
end_date = "2024-05-15"

options = uc.ChromeOptions()
 
# options.headless = False
# options.add_argument('--headless')
chrome_prefs = {
    "profile.default_content_setting_values": {
        "images": 0,
    }
}
options.experimental_options["prefs"] = chrome_prefs
# service = ChromeService(executable_path=ChromeDriverManager().install())
 
driver = uc.Chrome(options=options)

# driver = webdriver.Chrome()
driver.get(f"https://southfloridaopenhousesearch.com/open-houses?open_house_end_time_after={start_date}&open_house_end_time_before={end_date}")

url_array = []

try:
    driver.find_elements(By.TAG_NAME, "a")
except NoSuchElementException:
    print("Element not found, test passed.")
else:
    # raise AssertionError("Element was found, but should not exist!")
    elements = driver.find_elements(By.TAG_NAME, "a")
    for element in elements:
        url = element.get_attribute("href")
        print("url", url)
        if "/open-houses/FL" in url:
            print(url)
            url_array.append(url)
            
for url in url_array:
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_elements(By.CLASS_NAME, "swiper-wrapper")
    except NoSuchElementException:
        print("Element not found, test passed.")
    else:
        # raise AssertionError("Element was found, but should not exist!")
        element = driver.find_elements(By.CLASS_NAME, "swiper-wrapper")[0]
        img_urls = []
        try:
            element.find_elements(By.CLASS_NAME, "swiper-slide")
        except NoSuchElementException:
            print("Element not found, test passed.")
        else:
            img_divs = element.find_elements(By.CLASS_NAME, "swiper-slide")
            
            for img_div in img_divs:
                try:
                    img_div.find_element(By.TAG_NAME, "img")
                except NoSuchElementException:
                    print("no")
                else:
                    img = img_div.find_element(By.TAG_NAME, "img")
                    img_url = img.get_attribute("src")
                    img_urls.append(img_url)
        
        for img_url in img_urls:
            print(img_url)
            if img_url:
                response = requests.get(img_url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Extract the filename from the URL
                    img_filename = os.path.basename(img_url)

                    # Specify the local path to save the downloaded image
                    save_path = f"downloaded_images/{img_filename}"

                    # Save the image to the local filesystem
                    with open(save_path, "wb") as img_file:
                        img_file.write(response.content)
                        print(f"Image downloaded successfully: {save_path}")
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")

                
    
        
    
            
driver.quit()
