# -*- coding UTF-8 -*-

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen
from urllib.request import urlretrieve
from urllib.error import URLError, HTTPError

import pandas as pd

url = "https://alura-site-scraping.herokuapp.com/index.php"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

try:
    # Declarando variáveis
    cards = []

    # Obtendo o conteúdo do arquivo
    req = Request(url, headers = headers)
    response = urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    pages = int(soup.find('span', {"class": "info-pages"}).getText().split()[-1])

    for i in range(pages):
        
        # Obtendo o HTML
        response = urlopen(Request(url + "?page=" + str(i + 1), headers = headers))
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Obetendo as TAGs de interesse
        anuncios = soup.find('div', {"id": "container-cards"}).findAll('div', {'class': 'well card'})

        # Coletando as informações dos CARDs
        for anuncio in anuncios:
            card = {}

            # Valor
            card['value'] = anuncio.find('p', {'class': 'txt-value'}).getText()
            
            # Informações
            infos = anuncio.find('div', {'class': 'body-card'}).findAll('p')
            for info in infos:
                card[info.get('class')[0].split('-')[-1]] = info.getText()

            # Acessórios
            items = anuncio.find('div', {'class': 'body-card'}).ul.findAll('li')
            items.pop()
            acessorios = []
            for item in items:
                acessorios.append(item.getText().replace('? ', ''))
            card["items"] = acessorios

            # Imagens
            image = anuncio.find('div', {'class': 'image-card'}).img
            card["image"] = image.get('src')

            filename = image.get('src').split('/')[-1]
            urlretrieve(image.get('src'), './output/img/' + filename)

            # Adicionando resultado a lista cards
            cards.append(card)

    print(len(cards))

    # Criando um DataFrame com os resultados
    dataset = pd.DataFrame(cards)
    dataset.to_csv('./output/data/dataset.csv', sep=';', index = False, encoding = 'utf-8-sig')

    # dataset = pd.DataFrame.from_dict(card, orient = 'index').T

except HTTPError as e:
    print(e.status, e.reason)

except URLError as e:
    print(e.reason)
