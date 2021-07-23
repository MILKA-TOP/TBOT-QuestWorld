from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
from data import type_filter

menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
menu_filter_test = CallbackData("show_menu", "level", "category", "value", "not_one_result")
update_value = CallbackData("update", "category", "value", "type_keyboard")
page_checking = CallbackData("next_prev", "orientation", "page")
quest_page_checking = CallbackData("next_prev", "orientation", "page")
quest_open = CallbackData("quest", "index")


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, category="null", not_one_result="0", value="null"):
    return menu_filter_test.new(level=level, category=category, not_one_result=not_one_result, value=value)


def make_using_buttons(category="null", type_keyboard="null", value="null"):
    return update_value.new(category=category, type_keyboard=type_keyboard, value=value)


"""
ОБОЗНАЧЕНИЕ УРОВНЕЙ:

menu - основное меню фильтров
one_choice - только один выбор
more_choice - несколько выборов
level_check - проверка в несколько уровней
show - кнопка фильтрации
"""


async def categories_keyboard():
    type_filter_copy = type_filter
    categories = list(type_filter_copy.keys())

    inline_keyboard = [
        [InlineKeyboardButton(text="Показать квесты по фильтру", callback_data=make_callback_data(level="show"))],

        [InlineKeyboardButton(text=categories[0], callback_data=make_callback_data(level="one_choice",
                                                                                   category=
                                                                                   categories[0]))],

        [InlineKeyboardButton(text=categories[1], callback_data=make_callback_data(level="one_choice",
                                                                                   category=
                                                                                   categories[1])),
         InlineKeyboardButton(text=categories[2], callback_data=make_callback_data(level="one_choice",
                                                                                   category=
                                                                                   categories[2]))],

        [InlineKeyboardButton(text=categories[3], callback_data=make_callback_data(level="one_choice",
                                                                                   category=
                                                                                   categories[3])),
         InlineKeyboardButton(text=categories[4], callback_data=make_callback_data(level="level_check",
                                                                                   category=
                                                                                   categories[4]))],

        [InlineKeyboardButton(text=categories[5], callback_data=make_callback_data(level="one_choice",
                                                                                   category=
                                                                                   categories[5]))],

        [InlineKeyboardButton(text=categories[6], callback_data=make_callback_data(level="one_choice",
                                                                                   category=
                                                                                   categories[6]))],

        [InlineKeyboardButton(text=categories[7], callback_data=make_callback_data(level="more_choice",
                                                                                   category=
                                                                                   categories[7]))],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


async def subcategories_keyboard(category, updated_value):
    inline_keyboard = []
    type_keyboard = "subcategories"
    type_filter_copy = type_filter.get(category)
    categories = list(type_filter_copy.keys())

    for i in range(len(categories)):
        if not isinstance(updated_value, list):
            if categories[i] == updated_value:
                text = f"[{categories[i]}]"
            else:
                text = f"{categories[i]}"
        else:
            if type_filter_copy.get(categories[i]) in updated_value:
                text = f"[{categories[i]}]"
            else:
                text = f"{categories[i]}"
        if i % 2 == 0:
            row_keyboard = [InlineKeyboardButton(text=text, callback_data=make_using_buttons(
                value=type_filter_copy.get(categories[i]), category=category, type_keyboard=type_keyboard))]

            inline_keyboard.append(row_keyboard)
        else:
            inline_keyboard[i // 2].append(InlineKeyboardButton(text=text, callback_data=make_using_buttons(
                value=type_filter_copy.get(categories[i]), category=category, type_keyboard=type_keyboard)))

    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level="menu"))])
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


async def more_keyboards(category, updated_value, elements_keys, elements_values, start_number):
    type_keyboard = "more"
    inline_keyboard = []
    row_keyboard = []
    now_number = start_number
    while now_number < len(elements_keys) and (now_number - start_number) < 8:
        if now_number % 2 == 0:
            row_keyboard = [InlineKeyboardButton(text=elements_keys[now_number], callback_data=make_using_buttons(
                value=elements_values[now_number], category=category, type_keyboard=type_keyboard))]

        else:
            row_keyboard.append(InlineKeyboardButton(text=elements_keys[now_number], callback_data=make_using_buttons(
                value=elements_values[now_number], category=category, type_keyboard=type_keyboard)))
            inline_keyboard.append(row_keyboard)
        now_number += 1

    row_next_back = []
    if start_number != 0:
        row_next_back.append(InlineKeyboardButton(text="Обратно", callback_data=page_checking.new(orientation="back",
                                                                                                  page=start_number // 8)))
    if now_number != len(elements_keys):
        row_next_back.append(
            InlineKeyboardButton(text="Далее",
                                 callback_data=page_checking.new(orientation="next", page=start_number // 8)))
    if len(row_next_back) != 0:
        inline_keyboard.append(row_next_back)

    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level="menu"))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


async def quest_keyboard(quest_dict: dict, start_number):
    inline_keyboard = []
    now_number = start_number
    array_id = list(quest_dict.keys())
    while now_number < len(quest_dict) and (now_number - start_number) < 7:
        now_index = array_id[now_number]
        array_value = quest_dict.get(now_index)
        inline_keyboard.append(
            [InlineKeyboardButton(text=array_value[0], callback_data=quest_open.new(index=now_index))])
        now_number += 1

    row_next_back = []

    if start_number != 0:
        row_next_back.append(
            InlineKeyboardButton(text="Обратно", callback_data=quest_page_checking.new(orientation="back",
                                                                                       page=start_number // 7)))

    if now_number != len(array_id):
        row_next_back.append(
            InlineKeyboardButton(text="Далее",
                                 callback_data=quest_page_checking.new(orientation="next", page=start_number // 7)))
    if len(row_next_back) != 0:
        inline_keyboard.append(row_next_back)

    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data=make_callback_data(level="menu"))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)
