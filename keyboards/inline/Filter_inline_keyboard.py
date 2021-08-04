from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.utils.callback_data import CallbackData

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
from data import category_filter_dict, one_page_category_dict, more_pages_category_dict, ONE_PAGE_CATEGORY, \
    MORE_PAGES_CATEGORY, NEXT_PAGE_BUTTON, PREV_PAGE_BUTTON, MENU_INLINE_BUTTON, VALUE_CALLBACK, CATEGORY, \
    TYPE_CALLBACK, SHOW_QUEST_LIST_BUTTON, SHOW_QUEST, DEFAULT_PARAM, MENU_FILTER, DEFAULT_PARAM_BUTTON, NEXT_VALUE, \
    BACK_VALUE
from utils.parse.Filter_Parse import button_subcategory_text

filter_cd = CallbackData("filter_cd", TYPE_CALLBACK, VALUE_CALLBACK, CATEGORY)


def make_filter_callback(type_callback, value_callback="0", category="0"):
    return filter_cd.new(type_callback=type_callback, value_callback=value_callback, category=category)


async def categories_keyboard():
    type_filter_copy = category_filter_dict
    categories_list = list(type_filter_copy.keys())
    inline_keyboard = [
        [InlineKeyboardButton(text=SHOW_QUEST_LIST_BUTTON,
                              callback_data=make_filter_callback(type_callback=SHOW_QUEST))]]
    row_keyboard = []
    one_page_category_list = list(one_page_category_dict.keys())
    for i in range(len(categories_list)):
        if i % 2 == 0:
            row_keyboard = []
        level = str()
        if categories_list[i] in one_page_category_list:
            level = ONE_PAGE_CATEGORY
        elif categories_list[i] in more_pages_category_dict:
            level = MORE_PAGES_CATEGORY
        row_keyboard.append(InlineKeyboardButton(
            text=categories_list[i],
            callback_data=make_filter_callback(type_callback=level, category=categories_list[i])))

        if i % 2 != 0:
            inline_keyboard.append(row_keyboard)
    inline_keyboard.append([InlineKeyboardButton(text=DEFAULT_PARAM_BUTTON,
                                                 callback_data=make_filter_callback(type_callback=DEFAULT_PARAM))])
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
        [InlineKeyboardButton(text=MENU_INLINE_BUTTON,
                              callback_data=make_filter_callback(type_callback=MENU_FILTER))])

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

    row_next_back = []
    if start_number != 0:
        row_next_back.append(InlineKeyboardButton(
            text=PREV_PAGE_BUTTON,
            callback_data=make_filter_callback(type_callback="page_sub", category=category, value_callback=BACK_VALUE)))
    if now_number != len(elements_keys):
        row_next_back.append(
            InlineKeyboardButton(text=NEXT_PAGE_BUTTON,
                                 callback_data=make_filter_callback(type_callback="page_sub", category=category,
                                                                    value_callback=NEXT_VALUE)))
    if len(row_next_back) != 0:
        inline_keyboard.append(row_next_back)

    inline_keyboard.append(
        [InlineKeyboardButton(text=MENU_INLINE_BUTTON,
                              callback_data=make_filter_callback(type_callback=MENU_FILTER))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


back_menu_filter_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=MENU_INLINE_BUTTON, callback_data=make_filter_callback(type_callback=MENU_FILTER))]],
    resize_keyboard=True)
