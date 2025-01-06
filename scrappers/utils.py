from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

import os

CURRENT_PATH = os.getenv('PWD')

def generate_cookies(urls, sleep=10):
    service = Service(executable_path=f"{CURRENT_PATH}/geckodriver")
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options, service=service)
        
    for url in urls:
        driver.get(url)
        time.sleep(sleep)
    cookies = driver.get_cookies()
    print(cookies)  # List of all cookies
    driver.quit()
    return cookies