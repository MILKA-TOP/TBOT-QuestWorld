import requests
from bs4 import BeautifulSoup

from data import FILTER_QUESTS_POSTFIX, category_filter_dict, quest_difficult_demonstrate, \
    link_param_dict, param_text_by_user_text_dict
from data.Quest_Params import help_link_param_dict

"""
    Получение словарей "Многостраничных подкатегорий"
"""


def get_category_soup(main_city_link):
    filtered_link = main_city_link + FILTER_QUESTS_POSTFIX
    soup = BeautifulSoup(requests.get(filtered_link).text, 'html.parser')
    return soup.find('select', id="category_").find_all('option')


"""
    Составление фильтрованной ссылке по параметрам, введённым пользователем
"""


def add_params_to_link(settings, search_link):
    for elements in list(link_param_dict.keys()):
        checked_value = settings.get(elements)
        if isinstance(checked_value, list) and checked_value == [] or (
                not isinstance(checked_value, list) and str(checked_value) == "-1"):
            pass
        elif isinstance(checked_value, list):
            for array_value in checked_value:
                if elements not in help_link_param_dict:
                    search_link += link_param_dict.get(elements) + str(array_value) + "&"
                else:
                    search_link += link_param_dict.get(elements) + str(
                        help_link_param_dict.get(elements).get(array_value)) + "&"
        else:
            if elements not in help_link_param_dict:
                search_link += link_param_dict.get(elements) + str(checked_value) + "&"
            else:
                search_link += link_param_dict.get(elements) + str(
                    help_link_param_dict.get(elements).get(checked_value)) + "&"

    return search_link[:-1]


"""
    Получение словаря подкатегории "Жанр"
"""


def get_category_list(checked_link):
    soup_list = get_category_soup(checked_link)
    category_dict = dict()
    for i in range(len(soup_list)):
        category_dict[soup_list[i].text] = soup_list[i].get('value')

    return category_dict


"""
    Получение ключа словаря по его элементу
"""


def get_key(d, value):
    for k, v in d.items():
        if str(v) == str(value):
            return k


"""
    Формирование текста сообщения, где отображается название подкатегории и выбранные элементы данной подкатегории
"""


def get_text_category(filter_params: dict, more_pages_params: dict, category: str):
    text = "<b>" + category + "</b>: "

    now_dict = category_filter_dict.get(category)
    if now_dict is None:
        now_dict = more_pages_params.get(category)

    now_value = filter_params.get(param_text_by_user_text_dict.get(category))

    if isinstance(now_value, list) and now_value == []:
        text = text + "Любой\n"
    elif isinstance(now_value, list):
        for elements_array in now_value:
            text += str(get_key(now_dict, elements_array)) + ", "
        text = text[:-2] + "\n"
    else:
        text = text + str(get_key(now_dict, now_value)) + "\n"

    return text


"""
    Формирование текста сообщения с выбранными подкатегориями
"""


def get_text_now_choose(filter_params: dict, more_pages_params: dict, city: str):
    text = "<b>🏙 Выбранный город</b>: " + city + "\n" + "=" * 16 + "\n"
    i = 0
    filter_params = list(filter_params.values())
    for elements in list(category_filter_dict.keys()):
        text += "<b>" + elements + "</b>: "

        now_dict = category_filter_dict.get(elements)
        if now_dict is None:
            now_dict = more_pages_params.get(elements)

        if isinstance(filter_params[i], list) and filter_params[i] == []:
            text = text + "Любой\n\n"
        elif isinstance(filter_params[i], list):
            for elements_array in filter_params[i]:
                text += str(get_key(now_dict, elements_array)) + ", "
            text = text[:-2] + "\n\n"
        else:
            text = text + str(get_key(now_dict, filter_params[i])) + "\n\n"
        i += 1
    return text


"""
    Добавление или удаление символа `✅` с кнопки, которое зависит: выбрана ли соответствующая подкатегория или нет
"""


def button_subcategory_text(updated_value, subcategory, subcategory_dict):
    if not isinstance(updated_value, list):
        if str(subcategory_dict.get(subcategory)) == str(updated_value):
            text = f"✅ {subcategory}"
        else:
            text = f"{subcategory}"
    else:

        array_value = list(str(i) for i in updated_value)

        if str(subcategory_dict.get(subcategory)) in array_value:
            text = f"✅ {subcategory}"
        else:
            text = f"{subcategory}"

    return text


"""
Приведение параметров `now_number` к параметрам `array_value`
"""


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
