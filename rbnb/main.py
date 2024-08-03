import webbrowser
from playwright.sync_api import sync_playwright
import re

SBR_WS_CDP = 'wss://brd-customer-hl_5d56db18-zone-browser1:v562fvpm86hr@brd.superproxy.io:9222'


def open_debug_view(page):
    """Open the Bright Data Debug View"""
    
    client = page.context.new_cdp_session(page)
    frame_tree = client.send('Page.getFrameTree', {})
    frame_id = frame_tree['frameTree']['frame']['id']
    inspect = client.send('Page.inspect', {'frameId': frame_id})
    inspect_url = inspect['url']
    webbrowser.open(inspect_url)
    

def route_intercept(route):
    if route.request.resource_type == "image":
        return route.abort()
    return route.continue_()

def run(pw, bright_data=False, headless=False):
    print("Connecting to scrapping browser")
    
    if bright_data:
        browser = pw.chromium.connect_over_cdp(SBR_WS_CDP)
    else:
        browser = pw.chromium.launch(headless=headless)
        
    # context = browser.new_context()
    # context.set_default_timeout(60000)
    
        
    page = browser.new_page()
    
    page.route("**/*", route_intercept)
    
    if bright_data and not headless:
        open_debug_view(page)
    
    page.goto("https://www.airbnb.fr")
    page.wait_for_timeout(1000)
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
        next_page_button.click()

    page.wait_for_timeout(1000)
    browser.close()

if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(pw=playwright, bright_data=False, headless=False)