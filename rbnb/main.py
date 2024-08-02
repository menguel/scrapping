from playwright.sync_api import sync_playwright
import re

def run(pw):
    print("Connecting to scrapping browser")
    browser = pw.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.airbnb.fr")
    page.wait_for_timeout(10000)
    page.get_by_role("button", name="Continuer sans accepter").click()
    page.wait_for_timeout(1000)
    page.get_by_test_id("structured-search-input-field-query").click()
    page.wait_for_timeout(1000)
    page.get_by_test_id("structured-search-input-field-query").fill("rio")
    page.wait_for_timeout(1000)
    page.get_by_text("Rio de Janeiro, Brésil").click()
    page.wait_for_timeout(1000)
    page.locator("td").filter(has_text=re.compile(r"^5$")).nth(2).click()
    page.wait_for_timeout(1000)
    page.locator("td").filter(has_text=re.compile(r"^9$")).nth(2).click()
    page.wait_for_timeout(1000)
    page.get_by_test_id("structured-search-input-search-button").click()
    page.wait_for_timeout(1000)
    page_number = 1
    while True:
        print(f"Navigating to page {page_number}")
        next_page_button = page.get_by_label("Suivant", exact=True)
        if next_page_button.get_attribute("aria-disabled") == 'true': # On vérifie si l'on a attend la derniere page du catalogue
            break

        page_number += 1
        page.wait_for_timeout(1000)
        next_page_button.click

    page.wait_for_timeout(10000)
    browser.close()

if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(pw=playwright)