from aiogram.types import InlineKeyboardButton, InputMediaPhoto, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data import QUEST_LINE, offer_callback_params, QUEST_TELEGRAM_PAGE_COUNT, add_big_quest_params, PREV_PAGE_BUTTON, \
    NEXT_PAGE_BUTTON, MENU_INLINE_BUTTON, TO_INLINE_LIST_BUTTON, OFFER, QUEST, TYPE_CALLBACK, VALUE, FILTER, OFFER_TYPE, \
    OPEN_QUEST, PAGE, BACK_VALUE, NEXT_VALUE, MENU_FILTER, OPEN_ADD_INFO, BACK_LIST, BACK_QUEST, QUEST_BACK_INFO_BUTTON
from keyboards.inline.Filter_inline_keyboard import make_filter_callback
from utils.parse import get_quest_params_dict

offer_cd = CallbackData(OFFER, TYPE_CALLBACK, VALUE)
quest_cd = CallbackData(QUEST, TYPE_CALLBACK, VALUE)


def make_quest_filter_callback(type_callback, value="0"):
    return quest_cd.new(type_callback=type_callback, value=value)


def make_offer_callback_data(type_callback, value="0"):
    return offer_cd.new(type_callback=type_callback, value=value)


def quest_message_part(array_value, now_number):
    return get_quest_params_dict(array_value, now_number)


def offer_message_part(array_value: dict, number):
    array_value["number"] = number + 1
    return array_value


callback_func_dict = {
    QUEST: make_quest_filter_callback,
    FILTER: make_quest_filter_callback,
    OFFER: make_offer_callback_data
}

message_part = {
    QUEST: quest_message_part,
    OFFER: offer_message_part
}


async def main_universal_keyboard(input_dict: dict, start_number, message_text_format: str, type_callback: str,
                                  mod_value=4096):
    current_callback = callback_func_dict[type_callback]

    now_number = start_number
    inline_keyboard = []
    array_id = list(input_dict.keys())
    message = str()
    media = []
    message_part_func = message_part[type_callback]
    while (now_number % mod_value) < len(input_dict) and (
            now_number - start_number) < QUEST_TELEGRAM_PAGE_COUNT:
        now_id = array_id[now_number % mod_value]
        subcategory_value = input_dict.get(now_id)

        message_part_dict = message_part_func(subcategory_value, now_number)
        message += message_text_format.format(**message_part_dict)
        button_text = QUEST_LINE.format(numb=(now_number + 1), name=subcategory_value.get("name"))
        callback_type = offer_callback_params.get(subcategory_value.get(OFFER_TYPE))

        if type_callback == QUEST:
            callback_type = OPEN_QUEST
        inline_keyboard.append(
            [InlineKeyboardButton(text=button_text, callback_data=current_callback(callback_type, now_id))])

        if (now_number + 1) == len(input_dict) or (now_number - start_number) == 5:
            media.append(InputMediaPhoto(subcategory_value["link_img"], caption=message))
        else:
            media.append(InputMediaPhoto(subcategory_value["link_img"]))

        now_number += 1

    row_next_back = []
    if start_number != 0:
        row_next_back.append(
            InlineKeyboardButton(text=PREV_PAGE_BUTTON,
                                 callback_data=current_callback(type_callback=PAGE, value=BACK_VALUE)))

    if media and (type_callback != QUEST and now_number != len(
            input_dict) or type_callback == QUEST and now_number % 6 == 0):
        row_next_back.append(
            InlineKeyboardButton(text=NEXT_PAGE_BUTTON,
                                 callback_data=current_callback(type_callback=PAGE, value=NEXT_VALUE)))
    if row_next_back:
        inline_keyboard.append(row_next_back)

    if type_callback == QUEST:
        inline_keyboard.append(
            [InlineKeyboardButton(text=MENU_INLINE_BUTTON,
                                  callback_data=make_filter_callback(type_callback=MENU_FILTER))])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True), media


async def quest_add_params_keyboard(param_dict, callback_type=FILTER):
    inline_keyboard = []
    array = list(add_big_quest_params.keys())

    callback_func = callback_func_dict[callback_type]

    for element in array:
        if element in param_dict:
            callback_data = callback_func(OPEN_ADD_INFO, value=element)

            inline_keyboard.append([InlineKeyboardButton(text=add_big_quest_params[element],
                                                         callback_data=callback_data)])

    callback_data = callback_func(BACK_LIST)

    inline_keyboard.append(
        [InlineKeyboardButton(text=TO_INLINE_LIST_BUTTON, callback_data=callback_data)])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True)


async def get_main_quest_info_keyboard(callback_type: str):
    callback_func = callback_func_dict[callback_type]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=QUEST_BACK_INFO_BUTTON, callback_data=callback_func(BACK_QUEST))]],
        resize_keyboard=True)


temp_back_quest_menu_inline_markup_offer = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text=QUEST_BACK_INFO_BUTTON, callback_data=make_offer_callback_data(OPEN_QUEST))]],
    resize_keyboard=True)

back_list_offer_button = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text=TO_INLINE_LIST_BUTTON, callback_data=make_offer_callback_data(BACK_LIST))]],
    resize_keyboard=True)
