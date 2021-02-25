import requests
from bs4 import BeautifulSoup
import csv

"""Parser output of data in csv"""

url = 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/q-%D1%83%D0%BC%D0%B0%D0%BD%D1%8C-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B8/?page=1'


def site_snapshot(url):
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def check_main_block(snapshot,main_block, *args):
    array_search = snapshot.find_all(main_block, class_=args)
    return array_search


def pull_all(url):
    mainD = []
    for i in check_main_block(site_snapshot(url), 'tr', 'wrap'):
        lowD =[]
        # product name
        for ii in check_main_block(i, 'td', 'title-cell'):
            for iii in check_main_block(ii, 'strong'):
                lowD.append(iii.text)
                print(iii.text)
        # product price
        for ii in check_main_block(i, 'p', 'price'):
            for iii in check_main_block(ii, 'strong'):
                lowD.append(iii.text)
                print(iii.text)
        mainD.append(lowD)
    return mainD


def writen(listDate):
    myFile = open('example2.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(listDate)

pull_all(url)
listDate = []
soup = site_snapshot(url)
href_search = soup.find_all('a', class_='block br3 brc8 large tdnone lheight24')
for i in href_search:
    peg = i.get('href')
    Date = pull_all(peg)
    listDate = listDate + Date
writen(listDate)



