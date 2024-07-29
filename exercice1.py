from urllib.parse import urljoin # Permet de concatener les urls 
import requests 
from bs4 import BeautifulSoup
from pprint import pprint

BASE_URL = "https://books.toscrape.com/index.html"

def main(threshold: int = 5): # valeur seuil
    
    with requests.Session() as session: # Créer un session pour accelérer le programme 
    
        response = session.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # select est une méthode qui va nous permettre de selectionner des éléments grace au CSS 
        # soup.find("ul", class_="nav nav-list").find_all("a") #Quand t'on veut retrouver un element préci du html 
        
        # Alternative 
        categories = soup.select("ul.nav.nav-list a ") # select_one -> find() , select -> find_all()
        categories_url = [category["href"] for category in categories[1:]]
        pprint(categories_url)
        
        for i in categories_url:
            full_url = urljoin(BASE_URL, i)
            response = session.get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # soup.find_all("article", class_="product_pod")
            
            books = soup.select("article.product_pod")
            number_of_books = len(books)
            category_title = soup.select_one("h1").text
            if number_of_books <= threshold:
                print(f"La catégorie '{category_title}' ne contient pas assez de livres ({number_of_books}).")
                
            else:
                print(f"La catégorie '{category_title}' contient assez de livre ")

            
        

if __name__ == '__main__':
    main(threshold=5)