import re
import logging
from pathlib import Path  # for file management
import sys

import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

FILE_PATH = Path(__file__).parent / "airbnb.html"
logger = logging.getLogger(__name__)  # Pour créer un logueur
logging.basicConfig(level=logging.DEBUG)


def fetch_content(url: str,
                  from_disk: bool = False) -> str:  # Donner le choix à l'utilisateur de récupérer le html depuis le disque
    """ Fecth the content of the page with given url"""

    if from_disk and FILE_PATH.exists():
        return _read_from_file()

    try:
        logger.debug(f"Making request to {url}")
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        _write_to_file(content=html_content)
        return html_content
    except RequestException as e:
        logger.error(f"Couldn't fetch from {url} due to {str(e)}")
        raise


def get_average_price(html: str) -> int:
    """From the HTML, we get the average price"""

    prices = []

    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all('div', {'data-testid': "card-container"})
    # _1tyxjp1
    # _1y74zjx

    for div in divs:
        price = div.find('span', class_="_1y74zjx") or div.find('span', class_="_1tyxjp1")
        if not price:
            logger.warning(f"Couldn't find price in div {div}")
            continue

        price = re.sub(r"\D", "", price.text)
        if price.isdigit():  # Pour vérifier que l'on a des nombres
            logger.debug(f"Price found: {price}")
            prices.append(int(price))
        else:
            logger.warning(f"Price {price} is not a digit")
    return round(sum(prices) / len(prices)) if len(prices) else 0  # Calcule de la moyenne des prix et l'arrondi


def _write_to_file(content: str) -> bool:
    """ Write the content to a file """
    logger.debug("Writting content to file")
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    return FILE_PATH.exists()


def _read_from_file() -> str:
    """ Read the content from a file """
    logger.debug("Reading content from file")
    with open(FILE_PATH, "r") as f:
        return f.read()


if __name__ == "__main__":
    url = "https://www.airbnb.fr/s/Rio-de-Janeiro--Rio-de-Janeiro--Br%C3%A9sil/homes?tab_id=home_tab&monthly_start_date=2024-01-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&query=Rio%20de%20Janeiro,%20Br%C3%A9sil&date_picker_type=flexible_dates&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=one_month&adults=1&source=structured_search_input_header&search_type=autocomplete_click&price_filter_num_nights=28&place_id=ChIJW6AIkVXemwARTtIvZ2xC3FA"
    content = fetch_content(url=url, from_disk=True)
    average_price = get_average_price(html=content)
    print(average_price)
