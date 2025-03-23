import json
import os
import requests
from PIL import Image
from io import BytesIO



def download_and_convert(images):
    os.makedirs("downloaded_images", exist_ok=True)
    
    for index, url in enumerate(images):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            png_filename = f"downloaded_images/image_{index}.png"
            img.convert("RGBA").save(png_filename, "PNG")
            print(f"Saved: {png_filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

# Example usage
link = input('Enter Url pls :')
response = requests.get(link)
images = response.text.split('imgHttps = ')[1].split(';\n    const batoPass')[0]
image_links = json.loads(images)
download_and_convert(image_links)



