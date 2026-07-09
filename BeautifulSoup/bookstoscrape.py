
#importing important libraries BeautifulSoup, Request module, pandas,urllib.parse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests as req
import pandas as pd

BaseURL = 'https://books.toscrape.com'

with req.session() as session:
    result = session.get(BaseURL)
    result.raise_for_status()

    soup = BeautifulSoup(result.text,'html.parser')
articles = soup.find_all('article',class_="product_pod")
result = [
    {
        'Title': article.h3.a.get('title'),
        'Price': article.find('p',class_='price_color').text,
        'Availabilty': article.find('p',class_="instock availability").text.strip(),
        'URL': urljoin(BaseURL,article.h3.a.get('href'))
    }
    for article in articles
]


df = pd.DataFrame.from_records(result)
df.to_csv('./BeautifulSoup/booksData.csv',index=False)
#making a callout
# result = req.get(baseurl)
# context = result.text

# #parsing the html content to dom format
# soup = BeautifulSoup(context,'lxml')
# section = soup.find('section')
# articles = section.find_all('article')
# result = []
# for article in articles:
#     dic = {}
#     dic['Title'] =article.h3.a.get('title')
#     dic['Price']= article.find(class_="price_color").text
#     dic['Availability']=article.find(class_='instock availability').text.strip()
#     dic['Link']= baseurl+'/'+article.h3.a.get('href')
#     result.append(dic)
# df = pd.DataFrame.from_records(result)
# df.to_csv('booksData.csv',index=False)