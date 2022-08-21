import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv


agent = UserAgent()


with open('moscow_street.txt', 'w', encoding='windows-1251') as F:
    writer = csv.writer(F)
    writer.writerow([
        'street', 'house'
    ])


with open('moscow_streets.txt', 'w', encoding='utf-8') as F:
    writer = csv.writer(F)
    writer.writerow([
        'street', 'house'
    ])


def parse(agent=agent):
    url = 'http://mosopen.ru/streets/letter/1'
    response = requests.get(url=url, params={
        'user-agent': f'{agent.random}'
    }).text
    streets = BeautifulSoup(response, 'lxml').find_all('p', class_='alphabet clearfix')[0].find_all('a')
    links_streets = list()
    for street in streets:
        links_streets.append(street.get('href'))

    for url in links_streets:
        response = requests.get(url=url, params={
            'user-agent': f'{agent.random}'
        }).text
        soup = BeautifulSoup(response, 'lxml').find_all('div', class_='double_block clearfix')[0].find_all('li')
        link_dict = dict()
        for link in soup:
            link_dict[link.find('a').get('href')] = link.find('a').text
        for link in list(link_dict.items()):
            url = link[0]
            name = link[1]
            response = requests.get(url=url, params={
                'user-agent': f'{agent.random}'
            }).text
            soup = BeautifulSoup(response, 'lxml').find('h3').find_previous('p').find_all('a')
            for i in soup:
                try:
                    for j in ['аллея', 'улица', 'бульвар', 'деревня', 'квартал', 'линия', 'микрорайон', 'мост', 'шоссе', 'набережная', 'парк',
                                                  'переулок', 'площадь', 'посёлок', 'проезд', 'проектируемый проезд', 'просека', 'проспект', 'тупик']:
                        if j in i.get('title').lower():
                            full_name = i.get('title').split(', ')
                            street_name = full_name[0].capitalize()
                            house = ', '.join(full_name[1:]).capitalize().replace('"', '')
                            with open('moscow_street.txt', 'a', encoding='windows-1251') as F:
                                writer = csv.writer(F)
                                writer.writerow([
                                    street_name, house
                                ])
                                with open('moscow_streets.txt', 'a', encoding='utf-8') as F:
                                    writer = csv.writer(F)
                                    writer.writerow([
                                        street_name, house
                                    ])
                except Exception as ex:
                    print(ex)



parse()