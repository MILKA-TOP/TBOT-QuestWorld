import requests
from bs4 import BeautifulSoup

from data import FILTER_QUESTS_POSTFIX, array_params_link_params, category_filter_dict, quest_difficult_demonstrate, \
    link_param_dict
from utils.parse.ParseCitySite import get_quests


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


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
    for elements in list(link_param_dict.keys()):
        checked_value = settings.get(elements)
        if isinstance(checked_value, list) and checked_value == [] or (
                not isinstance(checked_value, list) and str(checked_value) == "-1"):
            pass
        elif isinstance(checked_value, list):
            for array_value in checked_value:
                search_link += link_param_dict.get(elements) + str(array_value) + "&"
        else:
            search_link += link_param_dict.get(elements) + str(checked_value) + "&"
    # for i in range(len(array_params_link_params)):
    #     # Параметры 1 и 7 являются массивами, поэтому их добавление в ссылку происходит поэлементного добавления из
    #     # списка
    #     if i == 2 and (str(settings[i]) == "-1" or settings[i] == '_'):
    #         pass
    #     elif i != 1 and i != 7:
    #         search_link += array_params_link_params[i] + str(settings[i]) + '&'
    #     else:
    #         for j in range(len(settings[i])):
    #             search_link += array_params_link_params[i] + str(settings[i][j]) + '&'
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
    category_dict = dict()
    for i in range(len(soup_list)):
        category_dict[soup_list[i].text] = soup_list[i].get('value')

    return category_dict


def get_key(d, value):
    for k, v in d.items():
        if str(v) == str(value):
            return k


def get_text_now_choose(filter_params: dict, more_pages_params: dict):
    text = ""
    i = 0
    filter_params = list(filter_params.values())
    for elements in list(category_filter_dict.keys()):
        text += "<b>" + elements + "</b>: "

        now_dict = category_filter_dict.get(elements)
        if now_dict is None:
            now_dict = more_pages_params.get(elements)

        if isinstance(filter_params[i], list) and filter_params[i] == []:
            text = text + "Любой\n"
        elif isinstance(filter_params[i], list):
            for elements_array in filter_params[i]:
                text += str(get_key(now_dict, elements_array)) + ", "
            text = text[:-2] + "\n"
        else:
            text = text + str(get_key(now_dict, filter_params[i])) + "\n"
        i += 1
    return text


def button_subcategory_text(updated_value, subcategory, subcategory_dict):
    if not isinstance(updated_value, list):
        if str(subcategory_dict.get(subcategory)) == str(updated_value):
            text = f"✅ {subcategory}"
        else:
            text = f"{subcategory}"
    else:

        is_digit_bool = is_digit(str(subcategory_dict.get(subcategory)))

        array_value = list(str(i) for i in updated_value)

        if str(subcategory_dict.get(subcategory)) in array_value:
            text = f"✅ {subcategory}"
        else:
            text = f"{subcategory}"

    return text


def get_quest_params_dict(array_value, now_number):
    quest_params_dict = dict()

    quest_params_dict["name"] = array_value["name"]
    quest_params_dict["number"] = str(now_number + 1)
    quest_params_dict["people_count"] = array_value["people_count"]
    quest_params_dict["difficulty_key"] = "🔑" * int(array_value["difficulty"])
    quest_params_dict["difficulty_word"] = quest_difficult_demonstrate[array_value["difficulty"] - 1]
    quest_params_dict["rating_num"] = array_value["rating"]
    quest_params_dict["rating_star"] = "⭐" * int(
        float(array_value["rating"][3:-1]) + (0.5 if float(array_value["rating"][3:-1]) > 0 else -0.5))
    return quest_params_dict
