import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()


def refresh():
    url = "https://cdn.apple-mapkit.com/ma/bootstrap?apiVersion=2&mkjsVersion=5.15.0&poi=1"
    response = requests.get(url, headers=headers)
    return response.json()['authInfo']['access_token']


def get_lat_apple(text):
    headers = {
        "accept": "*/*",
        "accept-language": "fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5",
        "authorization": f"Bearer {os.environ['token']}",
        "cache-control": "no-cache",
        "dnt": "1",
        "origin": "https://gps-coordinates.org",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://gps-coordinates.org/",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    url = "https://api.apple-mapkit.com/v1/geocode"
    params = {
        "q": text,
        "lang": "en-GB"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            return response.json()['results'][0]['center']['lat'], response.json()['results'][0]['center']['lng']
        except IndexError:
            print('IndexError')
            return get_lat(text.split(',')[1:])
    else:
        print('refresh')
        print(response.text)
        token = input('refresh: ')
        headers['authorization'] =f"Bearer {token}"
        return get_lat(text)


import requests
from urllib.parse import quote

def get_lat_long(address, api_key = '03c48dae07364cabb7f121d8c1519492'):
    # URL encode the address to handle spaces and special characters
    encoded_address = quote(address)
    
    # Construct the URL for the API request
    url = f'https://api.opencagedata.com/geocode/v1/json?q={encoded_address}&key={api_key}&no_annotations=1&language=en'
    
    # Set the headers for the request
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'fr-FR,fr;q=0.9,ar-DZ;q=0.8,ar;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'no-cache',
        'dnt': '1',
        'origin': 'https://www.gps-coordinates.net',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.gps-coordinates.net/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    
    # Send the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        try:
            return response.json()['results'][0]['geometry']['lat'], response.json()['results'][0]['geometry']['lng']  # Return the JSON response from the API
        except IndexError:
            print('IndexError')
            return get_lat_long(''.join(address.split(',')[1:]))
    else:
        print( f"Error: {response.status_code}, {response.text}")
        return f"Error: {response.status_code}, {response.text}"  # Return the error code if request fails



