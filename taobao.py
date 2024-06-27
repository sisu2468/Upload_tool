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

from PIL import Image
import io
import requests
import os

# Define your headers here
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

start_date = "2024-04-15"
end_date = "2024-05-15"

SCROLL_PAUSE_TIME = 0.5
REDUCED_SCROLL_HEIGHT = 800  # Define the amount to reduce the scroll height by

# Initialize Chrome WebDriver with specified options
driver = webdriver.Chrome()

# Set Chrome options
chrome_prefs = {
    "profile.default_content_setting_values": {
        "images": 0,
    }
}
options = webdriver.ChromeOptions()
options.experimental_options["prefs"] = chrome_prefs

# Load the webpage
driver.get("https://world.taobao.com/")

# Get the total scroll height
total_height = driver.execute_script("return document.body.scrollHeight")

# Calculate the reduced scroll height
reduced_scroll_height = total_height - REDUCED_SCROLL_HEIGHT

previous_height = 0
scroll_height = []
# Scroll down by the specified reduced scroll height until unable to scroll anymore
while True:
    # Scroll down by the specified reduced scroll height
    driver.execute_script("window.scrollBy(0, {});".format(REDUCED_SCROLL_HEIGHT))
    
    # Wait for a short period to allow the page to load
    time.sleep(SCROLL_PAUSE_TIME)
    
    # Calculate the new scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    # Break the loop if unable to scroll anymore
    scroll_height.append(new_height)
    # Assuming scroll_height is a list containing scroll heights
    if len(scroll_height) >= 7 and all(scroll_height[-1] == height for height in scroll_height[-7:]):
        break         
    
url_array = []
try:
    driver.find_elements(By.CLASS_NAME, "first-category-wrap")
    # Process the collected elements as needed
except NoSuchElementException:
    print("Element not found, test passed.")
else:
    # raise AssertionError("Element was found, but should not exist!")
    elements = driver.find_elements(By.CLASS_NAME, "first-category-wrap")
    for element in elements:
        data = element.get_attribute("data-spm")
        url = element.get_attribute("href")
        print("data", data)
        if "d1_Women_Apparel" in data or "d2_Men_Wear" in data:
            print(data)
            url_array.append(url)
print("data", url_array.__sizeof__())
for url in url_array:
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_elements(By.CLASS_NAME, "PicGallery--root--3CFJ5et")
    except NoSuchElementException:
        print("Element not found, test passed.")
    else:
        # raise AssertionError("Element was found, but should not exist!")
        element = driver.find_elements(By.CLASS_NAME, "PicGallery--root--3CFJ5et")[0]
        img_urls = []
        try:
            element.find_elements(By.CLASS_NAME, "PicGallery--mainPicWrap--1c9k21r")
        except NoSuchElementException:
            print("Element not found, test passed.")
        else:
            img_divs = element.find_elements(By.CLASS_NAME, "PicGallery--mainPicWrap--1c9k21r")
            
            for img_div in img_divs:
                try:
                    img_div.find_element(By.TAG_NAME, "img")
                except NoSuchElementException:
                    print("no")
                else:
                    img = img_div.find_element(By.TAG_NAME, "img")
                    img_url = img.get_attribute("src")
                    img_urls.append(img_url.replace("_Q75.jpg_.webp", ""))
        
        for img_url in img_urls:
            print(img_url)
            if img_url:
                response = requests.get(img_url, headers=headers)  # Include headers in the request

                if response.status_code == 200:
                    img_filename = os.path.basename(img_url)
                    img_filename = os.path.splitext(img_filename)[0] + '.jpg'
                    save_path = f"downloaded_images/{img_filename}"

                    # Load image from bytes, convert and save as JPEG
                    image = Image.open(io.BytesIO(response.content))
                    rgb_image = image.convert('RGB')  # Convert to RGB
                    rgb_image.save(save_path, 'JPEG')  # Save as JPEG

                    print(f"Image downloaded and converted successfully: {save_path}")
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")

driver.quit()
