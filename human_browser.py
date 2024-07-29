from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

"""
Playwright API nous sert à naviguer dans les site web avec un rendu dynamique il n'est 
pas en soi un outil pour faire du scrapping 
"""
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.docstring.fr/scraping/")
    # button = page.get_by_role("button", name="Récupérer les livres secrets")
    # button = page.locator("xpath=//html/body/button") # selection avec locator
    page.locator("css=#get-secrets-books").click()
    page.wait_for_timeout(1000)
    # if button :
    #     button.click()
    #
    # page.wait_for_timeout(10000)

    # Utilisation avec BeautifulSoup
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    for titre in soup.select("h2"):
        print(titre.text)
    browser.close()

