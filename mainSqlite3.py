import requests
from bs4 import BeautifulSoup
import sqlite3

"""Parser output of data in sqlite3 + uniqueness check"""

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

def writen(lowD):
    conn = sqlite3.connect('chat.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
       text INT PRIMARY KEY,
       step2 TEXT);
    """)
    conn.commit()

    query = """INSERT INTO users(text, step2)
       VALUES(?, ?);"""
    for i in lowD:
        try:
            cur.execute(query, i)
            conn.commit()
        except:
            print('Уже в БД')



pull_all(url)
listDate = []
soup = site_snapshot(url)
href_search = soup.find_all('a', class_='block br3 brc8 large tdnone lheight24')
for i in href_search:
    peg = i.get('href')
    Date = pull_all(peg)
    listDate = listDate + Date
writen(listDate)


