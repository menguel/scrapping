import webbrowser
from bs4 import BeautifulSoup
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
    
    # page.route("**/*", route_intercept)
    
    if bright_data and not headless:
        open_debug_view(page)
    url = "https://www.airbnb.fr/s/Rio-de-Janeiro--Rio-de-Janeiro--Br%C3%A9sil/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-10-01&price_filter_input_type=0&channel=EXPLORE&query=Rio%20de%20Janeiro%2C%20Br%C3%A9sil&place_id=ChIJW6AIkVXemwARTtIvZ2xC3FA&location_bb=wbX34MIsYzvBuKhowi8uJA%3D%3D&date_picker_type=monthly_stay&adults=1&source=structured_search_input_header&search_type=autocomplete_click"
    page.goto(url)
    page.get_by_role("button", name="Continuer sans accepter").click()
    # page.get_by_test_id("structured-search-input-field-query").click()
    # page.get_by_test_id("structured-search-input-field-query").fill("Rio de janeiro")
    # page.get_by_test_id("option-0").click()
    # page.get_by_test_id("expanded-searchbar-dates-months-tab").click()
    # page.get_by_test_id("monthly-dial-dot-1").click()
    # page.get_by_test_id("structured-search-input-field-guests-button").click()
    # page.get_by_test_id("stepper-adults-increase-button").click()
    # page.get_by_test_id("structured-search-input-search-button").click()
    # page.get_by_test_id("little-search").click()
    
    html_content = page.content() # Pour voir le contenu de la page 
    soup = BeautifulSoup(html_content, "html.parser")
    print(soup.prettify())
        
    browser.close()

if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(pw=playwright, bright_data=False, headless=False)