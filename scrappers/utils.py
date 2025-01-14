from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import json
import os
import glob
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

def read_json(path):
    with open(path,'r') as file:
        data = json.loads(file.read())
        return data

def concat():
    import pandas as pd
    import glob

    # Define the file pattern (adjust path and extension as needed)
    file_pattern = "./louay-data/*/*.csv"

    # List all files matching the pattern
    file_list = glob.glob(file_pattern)
    print(file_list)
    # Initialize an empty list to hold DataFrames
    dataframes = []

    # Read each file and append to the list
    for file in file_list:
        df = pd.read_csv(file)  # Use pd.read_excel(file) for Excel files
        dataframes.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the concatenated DataFrame to a new file
    combined_df.to_csv("./yellowpages.csv", index=False)