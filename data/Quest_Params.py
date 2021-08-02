def age_dict(years_dict: dict):
    out_dict = {"Любой": -1}
    for element in list(years_dict.values()):
        out_dict["🧍‍♂️-" + str(element)] = "alone-" + str(element)
        out_dict["👨‍👩‍👦 -" + str(element)] = "supervised-" + str(element)
    return out_dict


"""default_params_quest_filter = {'sort': 'default', "quest_types": [], "players": -1, "rating": -1, "min_age": -1,
                               "scary_level": -1, "level": -1, "category_sub": []}

array_params_link_params = ["sort=", "quest_types[]=", "players=", "rating=", "min_age=", "scary_level=", "level=",
                            "category[]="]

filter_type = ["sort", "quest_types", "players", "rating", "min_age", "scary_level", "level", "category_sub"]"""

quest_sort = {"По умолчанию": "default", "По популярности": "popularity", "По народному рейтингу": "rating",
              "По отзывам": "reviews"}

quest_types = {"Квест в реальности": 1, "Перформанс": 2, "Экшн-игра": 6, "VR-квест": 7}

players = {"Любое": -1, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10+": 10, "15+": 15}

rating = {"Любой": -1, "6+": 6, "6.5+": 6.5, "7+": 7, "7.5+": 7.5, "8+": 8, "8.5+": 8.5, "9+": 9, "9.5+": 9.5}

parents = {"Без сопровождения": "alone", "С родителями": "supervised"}

age = {"6+": 6, "8+": 8, "10+": 10, "12+": 12, "14+": 14, "16+": 16, "18+": 18}

scary_level = {"Любая": -1, "Не страшный": 0, "Немного страшный": 1, "Страшный": 2, "Очень страшный": 3}

quest_difficult_filter = {"Любая": -1, "Простой": "easy", "Средний": "moderate", "Сложный": "hard"}
quest_difficult_demonstrate = ["Простой", "Средний", "Сложный", "Очень сложный"]

"""category_filter_dict = {"Сортировать": quest_sort, "Тип игры": quest_types, "Количество человек": players,
                        "Народный рейтинг": rating, "Возраст игроков": age_dict(age), "Страшность": scary_level,
                        "Сложность": quest_difficult_filter, "Жанр": None}

one_page_category_dict = {"Сортировать": "sort", "Тип игры": "quest_types", "Количество человек": "players",
                          "Народный рейтинг": "rating", "Возраст игроков": "min_age",
                          "Страшность": "scary_level", "Сложность": "level"}

more_pages_category_dict = {"Жанр": "category_sub"}
"""

add_big_quest_params = {"details": "Детали", "description": "Описание"}

offer_callback_params = {"quest": "open_quest", "offer": "open_offer"}

QUEST_TELEGRAM_PAGE_COUNT = 6
SUBCATEGORIES_TELEGRAM_PAGE_COUNT = 8
MAX_MESSAGE_LENGTH = 4096


class FilterParameter(object):
    def __init__(self, user_text, param_text, subcategory_param, link_param, default_param, parameter_type):
        self.user_text = user_text
        self.param_text = param_text
        self.subcategory_param = subcategory_param
        self.link_param = link_param
        self.default_param = default_param
        self.parameter_type = parameter_type


all_array = [
    FilterParameter("Сортировать", "sort", quest_sort, "sort=", 'default', "one_page"),
    FilterParameter("Тип игры", "quest_types", quest_types, "quest_types[]=", [], "one_page"),
    FilterParameter("Количество человек", "players", players, "players=", -1, "one_page"),
    FilterParameter("Народный рейтинг", "rating", rating, "rating=", -1, "one_page"),
    FilterParameter("Возраст игроков", "min_age", age_dict(age), "min_age=", -1, "one_page"),
    FilterParameter("Страшность", "scary_level", scary_level, "scary_level=", -1, "one_page"),
    FilterParameter("Сложность", "level", quest_difficult_filter, "level=", -1, "one_page"),
    FilterParameter("Жанр", "category_sub", None, "category[]=", [], "more_pages"),
]

array_params_link_params = [i.link_param for i in all_array]
filter_type = [i.param_text for i in all_array]
default_params_array = [i.default_param for i in all_array]
default_params_quest_filter = dict(zip(filter_type, default_params_array))
link_param_dict = dict(zip(filter_type, array_params_link_params))
user_text_list = [i.user_text for i in all_array]
subcategory_param_list = [i.subcategory_param for i in all_array]
category_filter_dict = dict(zip(user_text_list, subcategory_param_list))
one_page_user_list = [i.user_text for i in all_array if i.parameter_type == "one_page"]
one_page_param_list = [i.param_text for i in all_array if i.parameter_type == "one_page"]
more_pages_user_list = [i.user_text for i in all_array if i.parameter_type == "more_pages"]
more_pages_param_list = [i.param_text for i in all_array if i.parameter_type == "more_pages"]
one_page_category_dict = dict(zip(one_page_user_list, one_page_param_list))
more_pages_category_dict = dict(zip(more_pages_user_list, more_pages_param_list))

all_category_dict_value = {**one_page_category_dict, **more_pages_category_dict}

type_filter_list = list(category_filter_dict.keys())