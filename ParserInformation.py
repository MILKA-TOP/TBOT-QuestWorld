from bs4 import BeautifulSoup
import requests

import FilteredTop
import Tools
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
filter_quests_postfix = "/quests/search?"
req = requests.get(original_url)
default_params_quest_filter = ['default', [], 0, 0, 0, 0, 0, []]
array_use_filter = ["Использовать настройки по умолчанию", "Применить фильтр"]
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
            quest_base = dict()
            city_name = input().lower().replace(' ', '-').replace('-', '')
            if city_name in quests_url[country_name]:

                # 'Городская' ссылка
                main_city_link = quests_url[country_name][city_name]

                # Ссылка на фильтрацию запросов
                filtered_link = main_city_link + filter_quests_postfix

                # Получение ссылки на квесты, отфильтрованные пользователем
                filtered_link = FilteredTop.use_filter(filtered_link,
                                                       BeautifulSoup(requests.get(filtered_link).text, 'html.parser'),
                                                       default_params_quest_filter)

                # Обработка всех страниц квестов, тчобы выдать полный результат и список квестов.
                page_number = 1
                while True:
                    temp_base = get_quests(main_city_link, filtered_link + "&page=" + str(page_number))
                    if len(temp_base) == 0:
                        break
                    quest_base = {**quest_base, **temp_base}
                    page_number += 1

            elif city_name == '0':
                break
    elif country_name == '0':
        break
