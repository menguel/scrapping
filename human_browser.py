from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

"""
Playwright API nous sert à naviguer dans les site web avec un rendu dynamique il n'est 
pas en soi un outil pour faire du scrapping 
"""
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Connexion à Instagram
    page.goto("https://www.instagram.com/accounts/login/")
    page.wait_for_selector('input[name="username"]')
    page.fill('input[name="username"]', "votre_nom_utilisateur")
    page.fill('input[name="menguel"]', "votre_mot_de_passe")
    page.click('button[type="submit"]')
    page.wait_for_navigation()
    
    # Navigation vers le site de scraping
    page.goto("https://www.docstring.fr/scraping/")
    page.locator("css=#get-secrets-books").click()
    page.wait_for_timeout(1000)

    # Utilisation avec BeautifulSoup
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    for titre in soup.select("h2"):
        print(titre.text)
    browser.close()

