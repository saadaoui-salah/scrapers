from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options

# Configure Firefox for headless mode

def generate_cookies(urls, sleep=10):
    firefox_options = Options()
    firefox_options.headless = True  # Run Firefox in headless mode
    driver = webdriver.Firefox(options=firefox_options)
        
    for url in urls:
        driver.get(url)
        time.sleep(sleep)
    cookies = driver.get_cookies()
    print(cookies)  # List of all cookies
    driver.quit()
    return cookies