from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.utils.callback_data import CallbackData

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
from data import category_filter_dict, QUEST_DESCRIBE, add_big_quest_params, one_page_category_dict, \
    more_pages_category_dict, ONE_PAGE_CATEGORY_TEXT, MORE_PAGES_CATEGORY_TEXT, QUEST_TELEGRAM_PAGE_COUNT, QUEST_LINE
from keyboards.inline.Offer_keyboard import make_offer_callback_data
from utils.parse.Filter_Parse import button_subcategory_text, get_quest_params_dict

filter_cd = CallbackData("filter_cd", "type_callback", "value_callback", "category")
quest_cd = CallbackData("quest", "type_callback", "value")

"""
    "open_quest": show_quest,
    "open_add_info": answer_add_quest_params,
    "back_quest": back_to_quest_info,
    "page_quests": update_keyboard_page,
    "back_list": back_quest_list1
"""


def make_filter_callback(type_callback, value_callback="0", category="0"):
    return filter_cd.new(type_callback=type_callback, value_callback=value_callback, category=category)


def make_quest_filter_callback(type_callback, value="0"):
    return quest_cd.new(type_callback=type_callback, value=value)


"""
ОБОЗНАЧЕНИЕ type_callback:

menu_filter - основное меню фильтров
one_sub - одна страница
more_sub - несколько страниц
page_sub - выбор страниц с value = next/prev
upd_val - обновить данные
show_quest - кнопка фильтрации
"""


async def categories_keyboard():
    type_filter_copy = category_filter_dict
    categories_list = list(type_filter_copy.keys())
    inline_keyboard = [
        [InlineKeyboardButton(text="Показать квесты по фильтру",
                              callback_data=make_filter_callback(type_callback="show_quest"))]]
    row_keyboard = []
    one_page_category_list = list(one_page_category_dict.keys())
    for i in range(len(categories_list)):
        if i % 2 == 0:
            row_keyboard = []
        level = ""
        if categories_list[i] in one_page_category_list:
            level = ONE_PAGE_CATEGORY_TEXT
        elif categories_list[i] in more_pages_category_dict:
            level = MORE_PAGES_CATEGORY_TEXT
        row_keyboard.append(InlineKeyboardButton(
            text=categories_list[i],
            callback_data=make_filter_callback(type_callback=level, category=categories_list[i])))

        if i % 2 != 0:
            inline_keyboard.append(row_keyboard)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


async def subcategories_one_page_keyboard(category, updated_value):
    inline_keyboard = []
    row_keyboard = []

    subcategory_dict = category_filter_dict.get(category)
    subcategories_key_list = list(subcategory_dict.keys())

    for i in range(len(subcategories_key_list)):

        text = button_subcategory_text(updated_value, subcategories_key_list[i], subcategory_dict)

        if i % 2 == 0:
            row_keyboard = []

        row_keyboard.append(
            InlineKeyboardButton(text=text, callback_data=make_filter_callback(type_callback="upd_val",
                                                                               value_callback=subcategory_dict.get(
                                                                                   subcategories_key_list[i]),
                                                                               category=category)))
        if i % 2 != 0:
            inline_keyboard.append(row_keyboard)

    inline_keyboard.append(
        [InlineKeyboardButton(text="К меню", callback_data=make_filter_callback(type_callback="menu_filter"))])
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


async def subcategories_more_page_keyboards(category, updated_value: list, elements_dict: dict, start_number,
                                            page_buttons_count):
    inline_keyboard = []
    row_keyboard = []
    elements_keys = list(elements_dict.keys())
    elements_values = list(elements_dict.values())
    now_number = start_number
    while now_number < len(elements_keys) and (now_number - start_number) < page_buttons_count:

        text = button_subcategory_text(updated_value, elements_keys[now_number], elements_dict)

        if now_number % 2 == 0:
            row_keyboard = []
        row_keyboard.append(
            InlineKeyboardButton(text=text, callback_data=make_filter_callback(type_callback="upd_val",
                                                                               value_callback=elements_values[
                                                                                   now_number], category=category)))

        if now_number % 2 != 0:
            inline_keyboard.append(row_keyboard)
        now_number += 1

    category_callback = more_pages_category_dict.get(category)
    row_next_back = []
    if start_number != 0:
        row_next_back.append(InlineKeyboardButton(
            text="Обратно",
            callback_data=make_filter_callback(type_callback="page_sub", category=category, value_callback="back")))
    if now_number != len(elements_keys):
        row_next_back.append(
            InlineKeyboardButton(text="Далее",
                                 callback_data=make_filter_callback(type_callback="page_sub", category=category,
                                                                    value_callback="next")))
    if len(row_next_back) != 0:
        inline_keyboard.append(row_next_back)

    inline_keyboard.append(
        [InlineKeyboardButton(text="К меню", callback_data=make_filter_callback(type_callback="menu_filter"))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


async def quest_keyboard(all_quest_dict: dict, minimum_quest_number):
    checked_page = minimum_quest_number // 12
    inline_keyboard = []
    now_quest_number = minimum_quest_number
    array_id = list(all_quest_dict.keys())
    media_group_array = []
    message = str()

    while (now_quest_number % 12) < len(all_quest_dict) and (
            now_quest_number - minimum_quest_number) < QUEST_TELEGRAM_PAGE_COUNT:
        now_index = array_id[now_quest_number % 12]
        array_value = all_quest_dict.get(now_index)

        message_quest = QUEST_DESCRIBE
        quest_params_dict = get_quest_params_dict(array_value, now_quest_number % 12 + checked_page * 12)

        message += message_quest.format(**quest_params_dict)
        text_button = QUEST_LINE.format(
            numb=now_quest_number % 12 + 1 + checked_page * 12,
            name=array_value["name"])

        inline_keyboard.append(
            [InlineKeyboardButton(text=text_button, callback_data=make_quest_filter_callback("open_quest", value=now_index))])

        if (now_quest_number + 1) == len(all_quest_dict) or (now_quest_number + 1 - minimum_quest_number) == 6:
            media_group_array.append(InputMediaPhoto(array_value["link_img"], caption=message))
        else:
            media_group_array.append(InputMediaPhoto(array_value["link_img"]))
        now_quest_number += 1

    row_next_back = []
    # page_quest
    if minimum_quest_number != 0:
        row_next_back.append(
            InlineKeyboardButton(
                text="Обратно",
                callback_data=make_quest_filter_callback("page_quests", value="back")))

    if media_group_array and now_quest_number % 6 == 0:
        row_next_back.append(
            InlineKeyboardButton(text="Далее",
                                 callback_data=make_quest_filter_callback("page_quests", value="next")))
    if row_next_back:
        inline_keyboard.append(row_next_back)

    inline_keyboard.append(
        [InlineKeyboardButton(text="К меню", callback_data=make_filter_callback(type_callback="menu_filter"))])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True), media_group_array, message


async def quest_add_params_keyboard(param_dict, callback_type="filter"):
    inline_keyboard = []
    array = list(add_big_quest_params.keys())
    for element in array:
        if element in param_dict:
            if callback_type == "filter":
                callback_data = make_quest_filter_callback("open_add_info", value=element)
            else:
                callback_data = make_offer_callback_data("open_add_info", value=element)
            inline_keyboard.append([InlineKeyboardButton(text=add_big_quest_params[element],
                                                         callback_data=callback_data)])
    if callback_type == "filter":
        callback_data = make_quest_filter_callback("back_list")
    else:
        callback_data = make_offer_callback_data("back_list")

    inline_keyboard.append(
            [InlineKeyboardButton(text="Назад", callback_data=callback_data)])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


back_quest_menu_inline_markup = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Назад", callback_data=make_quest_filter_callback("back_quest"))]], resize_keyboard=True)

back_menu_filter_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="К меню", callback_data=make_filter_callback(type_callback="menu_filter"))]],
    resize_keyboard=True)
