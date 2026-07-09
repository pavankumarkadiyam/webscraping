from bs4 import BeautifulSoup
import requests as req
import pandas as pd

baseurl = 'https://books.toscrape.com'
result = req.get(baseurl)
context = result.text

soup = BeautifulSoup(context,'lxml')
section = soup.find('section')
articles = section.find_all('article')
result = []
for article in articles:
    dic = {}
    dic['Title'] =article.h3.a.get('title')
    dic['Price']= article.find(class_="price_color").text
    dic['Availability']=article.find(class_='instock availability').text.strip()
    dic['Link']= article.h3.a.get('href')
    result.append(dic)
df = pd.DataFrame.from_records(result)
df.to_csv('booksData.csv',index=False)