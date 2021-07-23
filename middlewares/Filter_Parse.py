import requests
from bs4 import BeautifulSoup

from data import FILTER_QUESTS_POSTFIX, array_params_link
from middlewares import get_quests


def get_filter_soup(main_city_link):
    filtered_link = main_city_link + FILTER_QUESTS_POSTFIX
    soup = BeautifulSoup(requests.get(filtered_link).text, 'html.parser')
    array = soup.find('div', class_="filter-columns").find_all('div', "form-group")
    output_soup_array_first = array[0:2] + array[4:6]
    output_soup_array_sec = list(array[7])
    output_soup_array_sec.append(array[10:13])
    return output_soup_array_first + output_soup_array_sec


def get_category_soup(main_city_link):
    filtered_link = main_city_link + FILTER_QUESTS_POSTFIX
    soup = BeautifulSoup(requests.get(filtered_link).text, 'html.parser')
    return soup.find('select', id="category_").find_all('option')


def get_sort_type_list(sort_type_soup):
    out_sort_type_array = []
    for element in sort_type_soup:
        out_sort_type_array.append(element.text)
    return out_sort_type_array


def get_scroll_down_list(scroll_soup):
    text_scroll_list = []
    value_scroll_list = []
    for i in range(len(scroll_soup)):
        text_scroll_list.append(scroll_soup[i].text)
        value_scroll_list.append(scroll_soup[i].get('value'))

    return text_scroll_list, value_scroll_list


def get_sort_array(data):
    sort_type_soup = data.find_all('div', class_="radio")
    sort_type_array = get_sort_type_list(sort_type_soup)
    sort_type_value = []
    for element in sort_type_array:
        sort_type_value.append(sort_type_soup[element].find('input').get('value'))
    return sort_type_array[:-1], sort_type_soup[:-1]


def add_params_to_link(settings, search_link):
    for i in range(len(array_params_link)):
        # Параметры 1 и 7 являются массивами, поэтому их добавление в ссылку происходит поэлементного добавления из
        # списка
        if i == 2 and (settings[i] == -1 or settings[i] == '_'):
            pass
        elif i != 1 and i != 7:
            search_link += array_params_link[i] + str(settings[i]) + '&'
        else:
            for j in range(len(settings[i])):
                search_link += array_params_link[i] + str(settings[i][j]) + '&'
    return search_link[:-1]


def get_filter_quests_list(settings, search_link, main_link):
    link = add_params_to_link(settings, search_link) + "&page="
    quests = {}
    number_of_page = 1
    while True:
        new_quests_list = get_quests(main_link, link + str(number_of_page))
        if len(new_quests_list) == 0:
            # for i in quests:
            #    print(i)

            return quests
        quests.update(new_quests_list)
        number_of_page += 1


def get_category_list(checked_link):
    soup_list = get_category_soup(checked_link)
    text_scroll_list = []
    value_scroll_list = []
    for i in range(len(soup_list)):
        text_scroll_list.append(soup_list[i].text)
        value_scroll_list.append(soup_list[i].get('value'))

    return text_scroll_list, value_scroll_list
