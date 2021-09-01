import requests
from bs4 import BeautifulSoup

"""
    Составление словаря со списком всех городов и соответствующих ссылок
"""


def get_city_links(cities_soup_array):
    all_cities_links_dict = dict()
    pretty_cities_dict = dict()
    for country in cities_soup_array:
        out_city_dict = dict()

        array_city_soup = country.find_all('li')
        for element in array_city_soup:
            # Ниже страшная херня
            now_city_name = element.text.lower().replace('-', '')
            pretty_cities_dict[now_city_name] = element.text
            out_city_dict[now_city_name] = element.find('a').get('href')
        all_cities_links_dict.update(out_city_dict)

    return all_cities_links_dict, pretty_cities_dict


"""
    Обработка и получение `soup` из ссылки со списком всех городов
"""


def get_links_soup():
    original_url = "https://mir-kvestov.ru/cities"

    req = requests.get(original_url)

    data = BeautifulSoup(req.text, 'html.parser')

    return get_city_links(data.find_all('div', class_="col-sm-6"))
