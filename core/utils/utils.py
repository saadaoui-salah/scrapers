from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import json
import os
import glob
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
CURRENT_PATH = os.getenv('PWD')



async def generate_cookies(self, urls, sleep=10):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Change to True if you want headless mode
        context = await browser.new_context()
        page = await context.new_page()
        await page.wait_for_timeout(sleep*100)  # Wait for the page to load
        for url in urls:
            await page.goto(url)
            await page.wait_for_timeout(sleep*100)  # Wait for the page to load

        cookies = await context.cookies()
        self.cookies = []
        print(cookies)
        await browser.close()
        return cookies


def p(urls, sleep=10):
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

def read_json(path):
    with open(path,'r') as file:
        data = json.loads(file.read())
        return data

def read_json(path):
    with open(path,'r') as file:
        data = json.loads(file.read())
        return data

def read_csv(path):
    import pandas as pd
    df = pd.read_csv(path)
    df = df.where(pd.notnull(df), None)
    return df

def handle_nan(value):
    if isinstance(value, float) and np.isnan(value):  # Check if the value is NaN
        return None  # Replace NaN with None (SQL NULL)
    return value

