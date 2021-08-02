from aiogram.types import InlineKeyboardButton, InputMediaPhoto, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data import QUEST_TELEGRAM_PAGE_COUNT, OFFER_DESCRIBE, QUEST_LINE, offer_callback_params

offer_cd = CallbackData("offer", "type_callback", "value")


def make_offer_callback_data(type_callback, value="0"):
    return offer_cd.new(type_callback=type_callback, value=value)


"""
    open_offer; value = index
    open_quest; value = index
    page: value = next/back
"""


async def main_offer_keyboard(offers_dict: dict, start_offer_number):
    now_offer_number = start_offer_number
    inline_keyboard = []
    array_id = list(offers_dict.keys())
    message = str()
    media = []
    while now_offer_number < len(offers_dict) and (now_offer_number - start_offer_number) < QUEST_TELEGRAM_PAGE_COUNT:
        now_id = array_id[now_offer_number]
        offer_value = offers_dict.get(now_id)
        message += OFFER_DESCRIBE.format(**offer_value, number=now_offer_number + 1)
        button_text = QUEST_LINE.format(numb=(now_offer_number + 1), name=offer_value.get("name"))
        callback_type = offer_callback_params.get(offer_value.get("offer_type"))
        inline_keyboard.append(
            [InlineKeyboardButton(text=button_text, callback_data=make_offer_callback_data(callback_type, now_id))])

        if (now_offer_number + 1) == len(offers_dict) or (now_offer_number + 1 - start_offer_number) == 6:
            media.append(InputMediaPhoto(offer_value["link_img"], caption=message))
        else:
            media.append(InputMediaPhoto(offer_value["link_img"]))

        now_offer_number += 1
    row_next_back = []
    if start_offer_number != 0:
        row_next_back.append(
            InlineKeyboardButton(text="Обратно", callback_data=make_offer_callback_data(type_callback="page", value="back")))

    if now_offer_number != len(offers_dict):
        row_next_back.append(
            InlineKeyboardButton(text="Далее", callback_data=make_offer_callback_data(type_callback="page", value="next")))
    if row_next_back:
        inline_keyboard.append(row_next_back)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, resize_keyboard=True), media

back_quest_menu_inline_markup_offer = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Назад", callback_data=make_offer_callback_data("back_list", "0"))]], resize_keyboard=True)