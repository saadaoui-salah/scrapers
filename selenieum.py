import asyncio
from playwright.async_api import async_playwright
import os
import json

CURRENT_PATH = os.getenv('PWD')

email = 'moonvielle@gmail.com'
password = 'Eda11121988!'

async def generate_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Change to True if you want headless mode
        context = await browser.new_context()
        page = await context.new_page()
        
        # Facebook Login
        await page.goto('https://www.facebook.com/')
        await page.wait_for_selector("#email")
        await page.fill('#email', email)
        await page.fill('#pass', password)
        await page.click('button[name="login"]')
        await page.wait_for_timeout(5000)  # Wait for the page to load
        input('Please Solve the challenge and press enter')

        await page.goto('https://www.webtoons.com/member/login')
        await page.wait_for_timeout(5000)  # Wait for the page to load
        await page.click('._btnLoginSns.facebook')
        await page.wait_for_timeout(5000)  # Wait for the page to load
        await page.click("[role='button']")
        await page.wait_for_timeout(5000)  # Wait for the page to load

        input('Please Solve the challenge and press enter')

        # Get cookies after login
        cookies = await context.cookies()
        print(cookies)  # List of all cookies

        # Save cookies to a file
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)

        await browser.close()
        return cookies

#asyncio.run(generate_cookies())
