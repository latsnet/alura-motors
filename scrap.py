# -*- coding UTF-8 -*-

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen
from urllib.request import urlretrieve
from urllib.error import URLError, HTTPError

import pandas as pd

url = "https://alura-site-scraping.herokuapp.com/index.php"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

try:
    req = Request(url, headers = headers)
    response = urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    cards = []
    card = {}

    anuncio = soup.find('div', {'class': 'well card'})
    card['value'] = anuncio.find('p', {'class': 'txt-value'}).getText()
    
    infos = anuncio.find('div', {'class': 'body-card'}).findAll('p')
    for info in infos:
        card[info.get('class')[0].split('-')[-1]] = info.getText()

    items = anuncio.find('div', {'class': 'body-card'}).ul.findAll('li')
    items.pop()
    acessorios = []
    for item in items:
        acessorios.append(item.getText().replace('? ', ''))
    card["items"] = acessorios

    image = anuncio.find('div', {'class': 'image-card'}).img
    card["image"] = image.get('src')

    filename = image.get('src').split('/')[-1]
    urlretrieve(image.get('src'), './output/img/' + filename)

    print(card)

    # dataset = pd.DataFrame.from_dict(card, orient = 'index').T
    # dataset.to_csv('./output/data/dataset.csv', sep=';', index = False, encoding = 'utf-8-sig')

    


except HTTPError as e:
    print(e.status, e.reason)

except URLError as e:
    print(e.reason)
