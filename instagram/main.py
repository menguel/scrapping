import os
import re
import sys
from os.path import exists

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

COOKIES = [{'name': 'csrftoken', 'value': 'tq9q_8X4BcVNQmjwiNvkpO', 'domain': '.instagram.com', 'path': '/', 'expires': 1756083528.684469, 'httpOnly': False, 'secure': True, 'sameSite': 'None'}, {'name': 'wd', 'value': '1280x720', 'domain': '.instagram.com', 'path': '/', 'expires': 1725238732, 'httpOnly': False, 'secure': True, 'sameSite': 'Lax'}, {'name': 'mid', 'value': 'ZsvTSAAEAAHNMhR1h2MbkohcUjEA', 'domain': '.instagram.com', 'path': '/', 'expires': 1759193932, 'httpOnly': False, 'secure': True, 'sameSite': 'Lax'}, {'name': 'datr', 'value': 'SNPLZsLMUVnqQaxEyYuwKh-1', 'domain': '.instagram.com', 'path': '/', 'expires': 1759193934.759424, 'httpOnly': True, 'secure': True, 'sameSite': 'None'}, {'name': 'ig_did', 'value': 'D4C3DAFC-F165-4748-9244-4E87823F0889', 'domain': '.instagram.com', 'path': '/', 'expires': 1756169934.759614, 'httpOnly': True, 'secure': True, 'sameSite': 'None'}]


def login():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.instagram.com")
        page.wait_for_load_state("networkidle")
        page.get_by_label("Num. téléphone, nom d’").click()
        page.get_by_label("Num. téléphone, nom d’").fill("josephanovic")
        page.get_by_label("Mot de passe").click()
        page.get_by_label("Mot de passe").fill("menguel2684")
        page.locator("div").filter(has_text=re.compile(r"^Se connecter$")).first.click()
        cookies = context.cookies()
        print(cookies)
        page.wait_for_timeout(20000)

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        context.add_cookies(COOKIES)
        page.goto("https://www.instagram.com")
        page.wait_for_timeout(20000)
        browser.close()

        

if  __name__ == "__main__":
    main()
    

    