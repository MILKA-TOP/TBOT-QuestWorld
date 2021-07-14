import Tools
from Tools import get_num

# Получение списка типа сортировки квестов, который выводится пользователю
def get_sort_type_list(sort_type_soup):
    out_sort_type_array = []
    for element in sort_type_soup:
        out_sort_type_array.append(element.text)
    return out_sort_type_array


# Обработка запроса по типу сортировки квестов
def get_sort_type_value(data):
    sort_type_soup = data.find_all('div', class_="radio")
    sort_type_array = get_sort_type_list(sort_type_soup)
    Tools.console_out_array(sort_type_array)
    value = get_num(len(sort_type_array))
    return sort_type_soup[value].find('input').get('value')


# Получение списка типа квестов, который выводится пользователю
def get_type_game_value(data):
    input_types = []
    quest_type_soup = data.find_all('div', class_="checkbox")
    type_dict = dict()
    quest_type_array = get_sort_type_list(quest_type_soup)
    for i in range(len(quest_type_array)):
        type_dict[i] = quest_type_soup[i].find('input').get('value')
    while True:
        print("Повторный выбор позволяет удалить значение")
        print(input_types)
        Tools.console_out_array(quest_type_array)
        num_value = get_num(len(quest_type_array))
        if num_value == -1:
            break

        value = type_dict[num_value]
        if value in input_types:
            input_types.remove(value)
        else:
            input_types.append(value)

    return input_types


# Обработка запроса по типу квестов
def get_scroll_down_list(scroll_soup):
    text_scroll_list = []
    value_scroll_list = []
    for i in range(len(scroll_soup)):
        text_scroll_list.append(scroll_soup[i].text)
        value_scroll_list.append(scroll_soup[i].get('value'))

    return text_scroll_list, value_scroll_list


# Вывод списка количества человек/народного рейтинга/возраста игроков/страшности/сложности пользователю
def get_scroll_down_value(data):
    scroll_soup = data.find('select').find_all('option')
    scroll_list, scroll_value = get_scroll_down_list(scroll_soup)
    Tools.console_out_array(scroll_list)
    value = get_num(len(scroll_list))
    return scroll_value[value]


# Обработка запросов, связанных с количеством человек/народным рейтингом/возрастом игроков/страшности
# /сложности пользователя
def get_category_list(scary_level_soup):
    text_scary_level_list = []
    value_scary_level_list = []
    for i in range(len(scary_level_soup)):
        text_scary_level_list.append(scary_level_soup[i].text)
        value_scary_level_list.append(scary_level_soup[i].get('value'))

    return text_scary_level_list, value_scary_level_list


def get_category_value(data):
    input_types = []
    category_soup = data.find('select').find_all('option')
    category_list, category_value = get_scroll_down_list(category_soup)

    while True:
        print("Повторный выбор позволяет удалить значение")
        print(input_types)
        Tools.console_out_array(category_list)
        num_value = get_num(len(category_list))
        if num_value == -1:
            break

        value = category_value[num_value]
        if value in input_types:
            input_types.remove(value)
        else:
            input_types.append(value)
    return input_types


# Эта функция занимается созданием функции, которую мы дальше будем парсить и выводить пользователю.
def get_filtered_link(input_link, filter_data_array):
    array_params_link = ["sort=", "quest_types[]=", "players=", "rating=", "min_age=", "scary_level=", "level=",
                         "category[]="]
    for i in range(len(array_params_link)):
        # Параметры 1 и 7 являются массивами, поэтому их добавление в ссылку происходит поэлементного добавления из
        # списка
        if i == 2 and filter_data_array[i] == 0:
            pass
        elif i != 1 and i != 7:
            input_link += array_params_link[i] + str(filter_data_array[i]) + '&'
        else:
            for j in range(len(filter_data_array[i])):
                input_link += array_params_link[i] + str(filter_data_array[i][j]) + '&'
    return input_link[:-1]


# Обработка запросов, связанных с фильтрацией и сортировкой квестов определенного города
def use_filter(input_link, link_soup, filter_data_array):
    type_filter = ["Сортировать", "Тип игры", "Количество человек", "Народный рейтинг", "Возраст игроков", "Страшность",
                   "Сложность", "Жанр"]
    link_soup = link_soup.find('div', class_="filter-columns").find_all('div', "form-group")
    scroll_down_array = [-1, -1, 4, 5, 7, 10, 11, -1]

    while True:

        print(filter_data_array)
        Tools.console_out_array(type_filter)
        filter_number = get_num(len(type_filter))

        if filter_number == -1:
            return get_filtered_link(input_link, filter_data_array)

        elif filter_number == 0:
            filter_data_array[filter_number] = get_sort_type_value(link_soup[0])
        elif filter_number == 1:
            filter_data_array[filter_number] = get_type_game_value(link_soup[1])
        elif filter_number == 7:
            filter_data_array[filter_number] = get_category_value(link_soup[12])
        else:
            filter_data_array[filter_number] = get_scroll_down_value(link_soup[scroll_down_array[filter_number]])
