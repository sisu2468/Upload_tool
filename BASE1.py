# pyinstaller -F --paths=C:\Users\Administrator\Documents\WORK\scrape\.venv\Lib\site-packages BASE1.py --onefile --hide-console hide-early
import os
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import tkinter as tk
from tkinter import filedialog, simpledialog

class Scraping:
    def __init__(self, email, password, file_path):
        self.email = email
        self.password = password
        self.file_path = file_path
        
        self.options = webdriver.ChromeOptions()
        self.download_path = os.path.abspath(os.path.dirname(__file__))
        prefs = {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,  # Disable download prompt
            "safebrowsing.enabled": True,  # Enable safe browsing
        }
        self.options.add_experimental_option("prefs", prefs)

    def download_csv(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        
        url = "https://admin.thebase.com/staffs/login"
        self.driver.get(url)
        self.driver.implicitly_wait(20)
        actions = ActionChains(self.driver)
        
        try:
            # Find the input field by its name
            email_field = self.driver.find_element(By.NAME, "email")
            password_field = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.CLASS_NAME, "c-submitBtn__icon")
            
            # Enter email and password
            email_field.send_keys(self.email)
            password_field.send_keys(self.password)
            # Click login button
            login_button.click()
            
            type_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.c-submitBtn.c-submitBtn--full"))
            )
            type_button.click()
            time.sleep(5)
            logging.info("button clicked")
            
            self.driver.get("https://admin.thebase.com/apps/92/items")
            
            # Find the button with the specific 'for' attribute and click it
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input.m-uploadBox__input[accept="text/csv"]'))
            )
            
            file_input.send_keys(self.file_path)
            time.sleep(5)
            
            upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-submitBtn.button_bozYQUnI'))
            )
            
            print("upload")
            upload_button.click()

        except NoSuchElementException as e:
            logging.error(f"Element not found: {e}")
        except TimeoutException as e:
            logging.error(f"Timeout while waiting for element: {e}")
        finally:
            time.sleep(10)
            self.driver.quit()

def start_scraping():
    email = email_entry.get()
    password = password_entry.get()
    file_path = file_path_entry.get()
    scraper = Scraping(email, password, file_path)
    scraper.download_csv()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

# Set up the UI
root = tk.Tk()
root.title("在庫アップロードツール")

tk.Label(root, text="電子メール:").grid(row=0, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=0, column=1)

tk.Label(root, text="パスワード:").grid(row=1, column=0)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

tk.Label(root, text="CSVファイルパス:").grid(row=2, column=0)
file_path_entry = tk.Entry(root)
file_path_entry.grid(row=2, column=1)
tk.Button(root, text="ブラウズ", command=browse_file).grid(row=2, column=2)

tk.Button(root, text="在庫アップロード", command=start_scraping).grid(row=3, columnspan=3)

root.mainloop()
