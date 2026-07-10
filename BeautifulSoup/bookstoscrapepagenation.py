from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd


BASE_URL = 'https://books.toscrape.com'
result = []
with requests.Session() as session:
    currenturl = BASE_URL
    while currenturl:
        response = session.get(urljoin(BASE_URL,currenturl))
        response.raise_for_status()
        soup = BeautifulSoup(response.text,'html.parser')
        nexturl = soup.select_one('.pager .next a')
        if nexturl:
            currenturl = urljoin(currenturl,nexturl['href'])
        else:
            print(currenturl)
            currenturl = None
        articles = soup.find_all('article',class_="product_pod")
        result.extend([
            {
                'Title': article.select_one('h3 a')['title'], #article.h3.a.get('title')
                'Price': article.select_one('p.price_color').text,#find('p',class_='price_color').text,
                'Availabilty': article.select_one('p.instock.availability').text.strip(), #find('p',class_="instock availability")
                'URL': urljoin(BASE_URL,article.h3.a.get('href'))
            }
            for article in articles
        ])
print(len(result))
df = pd.DataFrame(result)
df.to_csv('BeautifulSoup/bookstoscrapewithpagenation.csv',index=False)

