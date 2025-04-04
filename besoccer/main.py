import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://fr.besoccer.com/"


def main():
    with requests.Session() as session:

        response = session.get(BASE_URL)


if __name__ == '__main__':
    main()