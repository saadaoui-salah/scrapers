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
    file_pattern = "./client-data/*.csv"

    # List all files matching the pattern
    file_list = glob.glob(file_pattern)
    # Initialize an empty list to hold DataFrames
    #dataframes = []

    # Read each file and append to the list
    # for file in file_list:
    #     dataframes.append(df)

    # Concatenate all DataFrames
    df = pd.read_csv('./r.csv')  # Use pd.read_excel(file) for Excel files
    # combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the concatenated DataFrame to a new file
    df.to_json("./res.json", index=False)


def add_lat():
    data = read_json('./res.json')
    print()
    new = []
    for i in data:
        pass

def get_lat_long(address):
    try:
        geolocator = Nominatim(user_agent="business_info_importer")
        location = geolocator.geocode(address)
        if location:
            return f"POINT({location.latitude} {location.longitude})"
        else:
            return None  # If no result is found, return None
    except Exception as e:
        print(f"Error during geocoding: {e}")
        return None

import mariadb

# Function to connect to the database
def connect_to_db():
    return mariadb.connect(
            host=os.environ['host'], 
            user=os.environ['user'],       
            password=os.environ['password'], 
            database=os.environ['database'] 
    )

def handle_nan(value):
    if isinstance(value, float) and np.isnan(value):  # Check if the value is NaN
        return None  # Replace NaN with None (SQL NULL)
    return value

# Function to insert data from CSV into the database
def insert_csv_to_db(file_path):
    # Connect to the database
    connection = connect_to_db()
    cursor = connection.cursor()

    # Read CSV into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Add missing columns with None (or NULL) values if they don't exist in the CSV
    columns = ['abn', 'availability', 'awards', 'business_name', 'category', 'contact_information', 'current_url', 
               'description', 'email', 'equipment_provided', 'experience', 'insurance_coverage', 'license_number', 
               'location', 'phone_number', 'primary_services', 'rating_avg', 'response_time', 'reviews', 
               'service_area', 'social_media', 'specializations', 'trade_type', 'website', 'lat_long']

    for col in columns:
        if col not in df.columns:
            df[col] = None  # Add missing column with None (will be inserted as NULL in DB)

    length = df.shape[0]
    # Insert rows into the database
    for index, row in df.iterrows():
        # Get lat-long from the location
        #lat_long = get_lat_long(row['location'])  # Replace 'location' with the correct column name for the address
        
        # Prepare the SQL query
        insert_query = """
        INSERT INTO business_information (
            abn, availability, awards, business_name, category, contact_information, current_url, description, email, 
            equipment_provided, experience, insurance_coverage, license_number, location, phone_number, primary_services, 
            rating_avg, response_time, reviews, service_area, social_media, specializations, trade_type, website, lat_long
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (
            handle_nan(row['abn']), handle_nan(row['availability']), handle_nan(row['awards']), handle_nan(row['business_name']),
            handle_nan(row['category']), handle_nan(row['contact_information']), handle_nan(row['current_url']),
            handle_nan(row['description']), handle_nan(row['email']), handle_nan(row['equipment_provided']),
            handle_nan(row['experience']), handle_nan(row['insurance_coverage']), handle_nan(row['license_number']),
            handle_nan(row['location']), handle_nan(row['phone_number']), handle_nan(row['primary_services']),
            handle_nan(row['rating_avg']), handle_nan(row['response_time']), handle_nan(row['reviews']),
            handle_nan(row['service_area']), handle_nan(row['social_media']), handle_nan(row['specializations']),
            handle_nan(row['trade_type']), handle_nan(row['website']), None  # Ensure lat_long is correctly formatted or None
        ))
        print(f'New item ({index} out of {length})')

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()


file_pattern = "./client-data/*.csv"

    # List all files matching the pattern
file_list = ['./client-data/hot.csv', './client-data/serviceseeking.csv', './client-data/truelocal.csv', './client-data/start.csv', './client-data/gumtree.csv', './client-data/hipages.csv']

#for f in file_list:
#    insert_csv_to_db(f)