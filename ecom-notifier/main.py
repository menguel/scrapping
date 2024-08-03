import os
import sys
from datetime import datetime
import json
from pathlib import Path
import urllib3

import requests
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

PRICE_FILEPATH  = Path(__file__).parent / "price.json"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger.remove()
logger.add(sys.stderr, level="DEBUG")
logger.add("logs/debug.log", level="WARNING", rotation="1 MB") # Dès que le fichier atteint 1 Mo on en crée un nouveau
def write_price_to_file(price: int):
    logger.info(f"Writing price {price} to file")

    if PRICE_FILEPATH.exists():
        with open(PRICE_FILEPATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(
        {
            "price": price,
            "timestamp": datetime.now().isoformat() # Format spécifique qui contient toute les informations dont on a besoin
        }
    )

    with open(PRICE_FILEPATH, "w") as f:
        json.dump(data, f, indent=4) # Ajout des données dans le fichier


def get_price_difference(current_price: int) -> int:
    logger.info(f"Getting price difference from {current_price}")
    if PRICE_FILEPATH.exists():
        with open(PRICE_FILEPATH, "r") as f:
            data = json.load(f)

        previous_price = data[-1]["price"]
    else:
        previous_price = current_price
    try:
        logger.info(f"Price difference from current price to previous price is {round(((previous_price-current_price) / (previous_price))*100)}%")
        return round(((previous_price-current_price) / (previous_price))*100)
    except ZeroDivisionError as e:
        logger.error("La varible previous_price contient la valeur zero")
        raise e

def send_alert(message: str):
    logger.info(f"Sending alert with message : {message}")
    try:
        response = requests.post("https://api.pushover.net/1/messages.json",
                             data={"token": os.environ["PUSHOVER_TOKEN"],
                                   "user": os.environ["PUSHOVER_USER"],
                                   "message": message}
                             )
    except requests.RequestException as e:
        logger.error(f"Coudn't send alert due to {str(e)}")
        raise e

def get_current_price(asin: str):
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

    proxies = {
        "http":  os.environ["PROXY"],
        "https": os.environ["PROXY"],
    }
    url = f"https://www.amazon.co.uk/dp/{asin}"
    try:
        response = requests.get(url, proxies=proxies, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Coudn't get price from {url} due to {str(e)}")
        raise e
    html_content = response.text

    tree = HTMLParser(html_content)
    price = tree.css_first("span.a-price-whole")
    print(price.text())
    if price:
        return int(price.text().replace(".", "")) # replace: pour remplacer le point par une chaine de caractère die
    error_msg = f"Couldn't find price in {url}"
    logger.error(error_msg)
    raise ValueError(error_msg)

def main(asin: str):
    current_price = get_current_price(asin=asin)
    price_diffence = get_price_difference(current_price=current_price)
    write_price_to_file(price=current_price)

    if price_diffence > 0:
        send_alert(f"Price has decreased by {price_diffence}%")


if __name__ == '__main__':
    asin = "B0CZSBLKLC"
    main(asin=asin)
    # write_price_to_file(100)
    # send_alert("Bonjour tout le monde")
