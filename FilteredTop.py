import Tools


def get_sort_type_list(sort_type_soup):
    out_sort_type_array = []
    for element in sort_type_soup:
        out_sort_type_array.append(element.text)
    return out_sort_type_array


def get_sort_type_value(data):
    sort_type_soup = data.find('div', class_="form-group").find_all('div', class_="radio")
    sort_type_array = get_sort_type_list(sort_type_soup)
    Tools.console_out_array(sort_type_array)
    value = get_num(len(sort_type_array))
    return sort_type_soup[value].find('input').get('value')


def get_type_game_list(quest_type_soup):
    out_quest_type_array = []
    for element in quest_type_soup:
        out_quest_type_array.append(element.text)
    return out_quest_type_array


def get_type_game_value(data):
    input_types = []
    quest_type_soup = data.find('div', class_="filter-columns").find_all('div', class_="form-group")[1].find_all('div',
                                                                                                                 class_="checkbox")
    while True:
        print("Повторный выбор позволяет удалить значение")
        print(input_types)
        quest_type_array = get_type_game_list(quest_type_soup)
        Tools.console_out_array(quest_type_array)
        num_value = get_num(len(quest_type_array))
        if num_value == -1:
            break

        value = quest_type_soup[num_value].find('input').get('value')
        if value in input_types:
            input_types.remove(value)
        else:
            input_types.append(value)

    return input_types


def get_num(max_number):
    print('Введите число от -1 до ' + (str(max_number - 1)))
    value = input().replace(' ', '')
    while not Tools.is_digit(value) or (value.isdigit() and (max_number <= int(value) or int(value) < -1)):
        print('Введите число от -1 до ' + (str(max_number - 1)))
        value = input().replace(' ', '')
    return int(value)


# Эта функция занимается созданием функции, которую мы дальше будем парсить и выводить пользователю.
def get_filtered_link(input_link, filter_data_array):
    array_params_link = ["sort=", "quest_types[]=", "players=", "rating=", "min_age=", "scary_level=", "level=",
                         "category[]="]
    for i in range(len(array_params_link)):
        # Параметры 1 и 7 являются массивами, поэтому их добавление в ссылку происходит поэлементного добавления из
        # списка
        if i != 1 and i != 7:
            input_link += array_params_link[i] + filter_data_array[i] + '&'
        else:
            for j in range(len(filter_data_array[i])):
                input_link += array_params_link[i] + filter_data_array[i][j] + '&'
    return input_link[:-1]


#    input_link += "sort=" + filter_data_array[0] + '&'
#    for i in range(len(filter_data_array[1])):
#        input_link += "quest_types[]=" + filter_data_array[1][i] + '&'
#    input_link += "players=" + filter_data_array[2] + '&'
#    input_link += "rating=" + filter_data_array[3] + '&'
#    input_link += "min_age=" + filter_data_array[4] + '&'
#    input_link += "scary_level=" + filter_data_array[5] + '&'
#    input_link += "level=" + filter_data_array[6] + '&'
#    for i in range(len(filter_data_array[7])):
#        input_link += "category[]=" + filter_data_array[7][i] + '&'


def use_filter(input_link, link_soup, filter_data_array):
    type_filter = ["Сортировать", "Тип игры", "Количество человек", "Народный рейтинг", "Возраст игроков", "Страшность",
                   "Сложность", "Жанр"]
    now_link = input_link
    while True:
        Tools.console_out_array(type_filter)
        filter_number = get_num(len(type_filter))
        if filter_number == -1:
            return now_link
        elif filter_number == 0:
            filter_data_array[filter_number] = get_sort_type_value(link_soup)
        elif filter_number == 1:
            filter_data_array[filter_number] = get_type_game_value(link_soup)
