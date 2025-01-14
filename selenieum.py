from selenium import webdriver
import time

# Set up the WebDriver (make sure to replace with the path to your WebDriver)
driver = webdriver.Firefox()

# Open the website
driver.get('https://sachane.com/markalar')

# Sleep for 10 seconds
input()

# Close the browser
driver.quit()


