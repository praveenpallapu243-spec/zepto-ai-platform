import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_rating(rating_class):
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for key in ratings:
        if key in rating_class:
            return ratings[key]
    return 3

def scrape_books():
    books = []
    for page in range(1, 4):
        p_url = f"http://books.toscrape.com/catalogue/page-{page}.html"
        resp = requests.get(p_url)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        articles = soup.find_all('article', class_='product_pod')
        for art in articles:
            title = art.h3.a['title']
            price_str = art.find('p', class_='price_color').text
            price_gbp = float(price_str.replace('£', '').strip())
            
            rating_class = art.find('p', class_='star-rating')['class']
            rating = parse_rating(rating_class)
            
            avail_str = art.find('p', class_='instock availability').text.strip()
            in_stock = 1 if "In stock" in avail_str else 0
            
            price_inr = round(price_gbp * 105.50, 2)
            
            books.append({
                "title": title,
                "price_gbp": price_gbp,
                "price_inr": price_inr,
                "rating": rating,
                "in_stock": in_stock,
                "category_name": "General Books"
            })
            
    df = pd.DataFrame(books)
    df.to_csv("cleaned_books.csv", index=False)
    print(f"Scraped and saved {len(df)} books successfully.")

if __name__ == "__main__":
    scrape_books()
