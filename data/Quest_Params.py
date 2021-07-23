default_params_quest_filter = ['default', [], -1, -1, -1, -1, -1, []]

array_params_link = ["sort=", "quest_types[]=", "players=", "rating=", "min_age=", "scary_level=", "level=",
                     "category[]="]

filter_type = ["sort", "quest_types", "players", "rating", "min_age", "scary_level", "level", "category"]

quest_sort = {"По умолчанию": "default", "По популярности": "popularity", "По народному рейтингу": "rating",
              "По отзывам": "reviews"}

quest_types = {"Квест в реальности": 1, "Перформанс": 2, "Экшн-игра": 6, "VR-квест": 7}

players = {"Любое": "_", "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10+": 10, "15+": 15}

rating = {"Любой": "_", "6+": 6, "6.5+": 6.5, "7+": 7, "7.5+": 7.5, "8+": 8, "8.5+": 8.5, "9+": 9, "9.5+": 9.5}

min_age = {"Без сопровождения": "alone", "С родителями": "supervised"}

age = {"6+": 6, "8+": 8, "10+": 10, "12+": 12, "14+": 14, "16+": 16, "18+": 18}

scary_level = {"Любая": "_", "Не страшный": 0, "Немного страшный": 1, "Страшный": 2, "Очень страшный": 3}

quest_difficult = {"Любая": "_", "Простой": "easy", "Средний": "moderate", "Сложный": "hard"}

type_filter = {"Сортировать": quest_sort, "Тип игры": quest_types, "Количество человек": players,
               "Народный рейтинг": rating, "Возраст игроков": [min_age, age], "Страшность": scary_level,
               "Сложность": quest_difficult, "Жанр": None}

not_one_param = ["Тип игры"]

type_filter_list = list(type_filter.keys())

