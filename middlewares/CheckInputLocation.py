import requests
from bs4 import BeautifulSoup


def get_city_links(cities_soup_array):
    out_country_dict = dict()

    for country in cities_soup_array:
        out_city_dict = dict()
        now_country_name = country.h3.text.lower().replace('-', '')

        array_city_soup = country.find_all('li')
        for element in array_city_soup:
            # Ниже страшная херня
            now_city_name = element.text.lower().replace('-', '')
            out_city_dict[now_city_name] = element.find('a').get('href')
        out_country_dict[now_country_name] = out_city_dict

    return out_country_dict


def get_soup():
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
    return quests_url

# def check_country():
