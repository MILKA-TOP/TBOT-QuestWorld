from bs4 import BeautifulSoup
import requests
from ParseCitySite import get_quests

"""def get_scary_level(url_quest):
    out_scary = data.find('span', class_="td scary")
    boolean = (len(out_scary.find_all('span', "rich-tooltip-1-title")) != 0)
    if boolean:
        return out_scary.find('span', "rich-tooltip-1-title").text
    return out_scary.text
"""


def get_city_links(cities_soup_array):
    out_country_dict = dict()

    for country in cities_soup_array:
        out_city_dict = dict()
        now_country_name = country.h3.text.lower().replace('-', '')

        array_city_soup = country.find_all('li')
        for element in array_city_soup:
            print(element)
            # Ниже страшная херня
            now_city_name = element.text.lower().replace('-', '')
            out_city_dict[now_city_name] = element.find('a').get('href')
        out_country_dict[now_country_name] = out_city_dict

    return out_country_dict


original_url = "https://mir-kvestov.ru/cities"
full_quests_postfix = "/quests"
req = requests.get(original_url)

data = BeautifulSoup(req.text, 'html.parser')

# Получение мапы, которая хранит в себе ссылки на сайты по квестам
# Страна -> Город -> Ссылка
quests_url = get_city_links(data.find_all('div', class_="col-sm-6"))

while True:
    print("Введите название страны")
    country_name = input().lower().replace(' ', '').replace('-', '')
    if country_name in quests_url:
        while True:
            print("Введите название города")
            city_name = input().lower().replace(' ', '-').replace('-', '')
            if city_name in quests_url[country_name]:
                main_city_link = quests_url[country_name][city_name]
                get_quests(main_city_link, main_city_link + full_quests_postfix)
            elif city_name == '0':
                break
    elif country_name == '0':
        break
