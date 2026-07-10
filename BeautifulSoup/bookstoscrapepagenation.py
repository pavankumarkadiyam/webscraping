from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd
import os
import time
OUTPUT_DIR = 'BeautifulSoup/bookstoscrapepagenation.csv'
BASE_URL = 'https://books.toscrape.com'

def parse_scrape(soup):
    articles = soup.find_all('article',class_="product_pod")
    books = [
        {
            'Title': article.select_one('h3 a').get('title','N/A'), #article.h3.a.get('title')
            'Price': article.select_one('p.price_color').text.strip(),#find('p',class_='price_color').text,
            'Availabilty': article.select_one('p.instock.availability').text.strip(), #find('p',class_="instock availability")
            'URL': urljoin(BASE_URL,article.h3.a.get('href',''))
        }
        for article in articles
    ]
    return books
def scrape():
    results = []
    with requests.Session() as session:
        currenturl = BASE_URL
        while currenturl:
            response = session.get(currenturl)
            response.raise_for_status()
            soup = BeautifulSoup(response.text,'html.parser')
            results.extend(parse_scrape(soup))
            nexturl = soup.select_one('.pager .next a')
            if nexturl:
                currenturl = urljoin(currenturl,nexturl['href'])
            else:
                currenturl = None
            time.sleep(0.5)
    return results
def main():
    os.makedirs(os.path.dirname(OUTPUT_DIR),exist_ok=True)
    df = pd.DataFrame(scrape())
    df.to_csv(OUTPUT_DIR,index=False,encoding='utf-8-sig')
if __name__ == '__main__':
    main()

