import sys
import re
from selectolax.parser import HTMLParser 
from typing import List
from urllib.parse import urljoin

from loguru import logger
import requests

logger.remove()
logger.add("books.log", rotation="500kb", level="WARNING")
logger.add(sys.stderr, level="INFO")

BASE_URL = "https://books.toscrape.com/index.html"

"""

Fonction pour les URLs de tous les livres de la bibliothèque
Fonction pour récupérer l'url de la page suivante
     - Récupérer à partir du html directement ou de l'URL ?
Fonction pour récupérer les URLs sur une page spécifique
 
"""


def get_all_books_url(url: str) -> List[str]:
    """
    Récupère touttes les URLs des livres sur toutes les pages à partir d'une URL

    :param url: URL de départ
    :return: Liste de toutes les URLs de toute les pages
    """
    urls = []
    with requests.Session() as session:
        while True:
            logger.info(f"Scrapping page at {url}")
            try:
                response = session.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(f"Erreur lors de la requête HTTP sur la page {url} : {e}")
                continue

            tree = HTMLParser(response.text)
            books_urls = get_all_books_urls_on_page(url, tree)
            urls.extend(books_urls)

            url = get_next_page_url(url, tree)
            if not url:
                break

    return urls



def get_next_page_url(url: str, tree: HTMLParser) -> str | None:
    """
    Récupère l'URL de la page suivante à partir d'une page donnée.

    :param url: URL de la page courante
    :param tree: Objet HTMLParser de la page
    :return: URL de la page suivante
    """

    next_page_node = tree.css_first("li.next > a")
    if next_page_node and "href" in next_page_node.attributes:
        return urljoin(url, next_page_node.attributes["href"])

    logger.info("Aucun bouton next trouver sur la page")
    return None

def get_all_books_urls_on_page(url: str, tree: HTMLParser) -> List[str]:
    """
    Récupère toute les URLs des livres présent sur une page
    :param url: URL de la page qui contient les livres
    :param tree: Objet HTMLParser de la page
    :return: Liste de URLs de tout les livres sur la page
    """
    try:
        books_links_nodes = tree.css("h3 > a")
        return [urljoin(url, link.attributes["href"]) for link in books_links_nodes if "href" in link.attributes]
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des livre : {e}")
        return []

"""

Fonction qui à partir de l'URL d'un livre, va calculer le prix
Fonction pour récupérer le prix à partir du HTML
Fonction pour récupérer la quantité disponible à partir du HTML

"""
def get_book_price(url: str, session: requests.Session = None) -> float: # None comme pour que la variable n'est pas obligatoire
    """
    Récupère le prix d'un livre à partir de son URLs
    :param url: URL de la page du livre
    :return: Prix du livre multiplié par le nombre de livres en stock
    """
    try:
        if session:
            response = session.get(url)
        else:
            response = requests.get(url)
        response.raise_for_status()
        tree = HTMLParser(response.text)
        price = extract_price_from_page(tree)
        stock = extract_stock_quantity_from_page(tree)
        price_stock = price * stock
        logger.info(f"Get book price at {url} : fond {price_stock}")
        return price_stock
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la requête HTTP : {e}")
        return 0.0


def extract_price_from_page(tree: HTMLParser) -> float:
    """
    Extrait le prix du livre depuis le code HTML de la page
    :param tree: Objet HTMLParser de la page du livre
    :return: Prix unitaire du livre
    """

    price_node = tree.css_first("p.price_color")
    if price_node:
        price_string = price_node.text()
    else:
        logger.error("Aucun aucun noeud contenant le prix n'a été trouvé.")
        return 0.0
    try:
        price = re.findall(r"[0-9.]+", price_string)[0]
    except IndexError as e:
        logger.error(f"Aucun nombre n'a été trouvé: {e}")
        return 0.0
    else:
        return float(price)


def extract_stock_quantity_from_page(tree: HTMLParser) -> int:
    """
    Extrait la quantité de livre en stock depuis le code HTML de la page
    :param tree: Objet HTMLParser de la page du livre
    :return: Le nombre de livres en stock
    """

    try :
        stock_node = tree.css_first("p.instock.availability")
        return int(re.findall(f"[0-9]+", stock_node.text())[0])
    except AttributeError as e:
        logger.error(f"Aucun noeud 'p.instock.availability' n'a été trouvé sur la page : {e}")
        return 0
    except IndexError as e:
        logger.error(f"Aucun nombre n'a été trouvé dans le noeud : {e}")
        return 0


def main():
    base_url = "https://books.toscrape.com/index.html"
    all_books_urls = get_all_books_url(url=base_url)
    total_price = 0
    with requests.Session() as session:
        for book_url in all_books_urls:
            price = get_book_price(url=book_url, session=session)
            total_price += price

    return total_price


if __name__ == "__main__":
    print(main())


