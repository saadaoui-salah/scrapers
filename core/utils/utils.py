import asyncio
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
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from threading import Thread
import queue

def generate_cookies(urls=["https://venda-imoveis.caixa.gov.br/"], sleep=10):
    result_queue = queue.Queue()

    def run():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            for url in urls:
                page.goto(url)
                page.wait_for_timeout(sleep * 100)  # 100ms unit
            cookies = context.cookies()
            browser.close()
            result_queue.put(cookies)

    t = Thread(target=run)
    t.start()
    t.join()
    return result_queue.get()


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

def read_csv(path):
    import pandas as pd
    df = pd.read_csv(path)
    df = df.where(pd.notnull(df), None)
    return df

def handle_nan(value):
    if isinstance(value, float) and np.isnan(value):  # Check if the value is NaN
        return None  # Replace NaN with None (SQL NULL)
    return value
