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
import scrapy
from typing import Union


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

def read_glob_files(pattern):
    files = glob.glob(f'./client-data/{pattern}')
    for file in files:
        with open(file, 'r') as f:
            sel = scrapy.Selector(text=f.read())
            yield sel

def fake_request(callback, meta=None):
    from scrapy import Request
    return Request(
        url="https://www.gogle.com/",
        callback=callback,
        dont_filter=True,
        meta=meta
    )

def read_json_files(pattern):
    files = glob.glob(f'./client-data/{pattern}')
    for file in files:
        yield read_json(file)

import requests

def fetch_sheet(sheet_id: str, sheet_name: str):
    """
    Fetch public Google Sheet data as JSON.

    Args:
        sheet_id (str): The Google Sheet ID (from the URL).
        sheet_name (str): The name of the sheet tab.

    Returns:
        list[dict]: List of rows as dictionaries with column headers as keys.
    """
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:json&sheet={sheet_name}"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch sheet: HTTP {response.status_code}")

    raw_data = response.text

    try:
        json_str = raw_data[raw_data.find("{"):-2]
        data = json.loads(json_str)
    except Exception as e:
        raise Exception("Failed to parse Google Sheet response") from e

    columns = [col["label"] for col in data["table"]["cols"]]
    rows = []

    for row in data["table"]["rows"]:
        values = [cell.get("v") if cell else None for cell in row["c"]]
        rows.append(dict(zip(columns, values)))

    return rows

def csv_to_dict(data: Union[str, pd.DataFrame]) -> list[dict]:
    """
    Convert a CSV file or pandas DataFrame to a list of dictionaries.

    Args:
        data (str | pd.DataFrame): Path to CSV file or a pandas DataFrame.

    Returns:
        list[dict]: List of rows as dictionaries.
    """
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"CSV file not found: {data}")
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise ValueError("Input must be a file path or a pandas DataFrame")

    return df.to_dict(orient='records')


