from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from data import OFFERS_BUTTON, OFFERS_QUESTS_POSTFIX, FORMAT_OUTPUT_QUEST
from data.Texts import OFFER_MESSAGE
from handlers.users.filter import delete_media_message, delete_new_params_from_quest
from handlers.users.start import update_data_user
from keyboards.inline.Filter_inline_keyboard import quest_add_params_keyboard
from keyboards.inline.Offer_keyboard import offer_cd, main_offer_keyboard, back_quest_menu_inline_markup_offer
from loader import dp
from utils.parse.Offers_Parse import get_offers_parse, get_full_offer_info
from utils.parse.ParseQuestSite import get_quest_params


@dp.message_handler(Command("offers") | Text(OFFERS_BUTTON))
async def show_offers_city(message: Message, state: FSMContext):
    data = await state.get_data()
    main_city_link = data.get("main_city_link")
    if len(data) == 0 or main_city_link is None:
        await update_data_user(state)
    data = await state.get_data()
    main_city_link = data.get("main_city_link")

    offers_dict = get_offers_parse(main_city_link + OFFERS_QUESTS_POSTFIX, main_city_link)
    if len(offers_dict) == 0:
        await message.answer("В вашем городе не было обнаружено акций")
    else:
        markup, media = await main_offer_keyboard(offers_dict, 0)
        offers_media_message = await message.answer_media_group(media)
        offers_message = await message.answer("Выберите акцию из списка", reply_markup=markup)
        await state.update_data(offers_dict=offers_dict)
        await state.update_data(offers_media_message=offers_media_message)
        await state.update_data(offers_message=offers_message)
        await state.update_data(offer_page=0)


"""
    open_offer; value = index
    open_quest; value = index
    page_check: value = next/back
"""


@dp.callback_query_handler(offer_cd.filter())
async def offer_navigate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    type_callback = callback_data.get("type_callback")
    value = callback_data.get("value")

    level = {
        "open_offer": show_another_offer,
        "open_quest": show_quest_offer,
        "page": change_offer_keyboard,
        "open_add_info": show_add_params_quest,
        "back_list": back_offer_list
    }

    function = level[type_callback]

    await function(call, state, value=value)


async def back_offer_list(call: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    await call.message.delete()

    offers_dict = data.get("offers_dict")
    page_number = data.get("offer_page")
    markup, media = await main_offer_keyboard(offers_dict, page_number * 6)

    await state.update_data(offers_media_message=(await call.message.answer_media_group(media)))
    filter_message = await call.message.answer("Выберите акцию из списка", reply_markup=markup)
    await state.update_data(offers_message=filter_message)


async def show_another_offer(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    index = int(value)
    offers_message = data.get("offers_message")
    await delete_media_message(data, "offers_media_message")
    await offers_message.delete()
    message = await call.message.answer("Загрузка. . .\n\n")
    offers_dict = data.get("offers_dict")
    offer_value = offers_dict[index]
    link = offer_value.get("link")
    text = OFFER_MESSAGE.format(**(get_full_offer_info(link)))
    await message.edit_text(text, reply_markup=back_quest_menu_inline_markup_offer)


async def show_quest_offer(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    index = int(value)
    offers_message = data.get("offers_message")
    await delete_media_message(data, "offers_media_message")
    await offers_message.delete()
    message = await call.message.answer("Загрузка. . .\n\n")
    offers_dict = data.get("offers_dict")
    quest_value = offers_dict[index]
    link = quest_value.get("link")
    quest_value.update(get_quest_params(link, full_info=True))
    markup = await quest_add_params_keyboard(quest_value, callback_type="offer")
    await message.edit_text(FORMAT_OUTPUT_QUEST.format(dif_text="difficulty", **quest_value), reply_markup=markup)


async def change_offer_keyboard(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    old_page = data.get("offer_page")
    offers_dict = data.get("offers_dict")
    if value == "next":
        old_page += 1
    elif value == "back":
        old_page -= 1
    markup, media = await main_offer_keyboard(offers_dict, old_page * 6)
    await delete_media_message(data, "offers_media_message")
    await (data.get("offers_message")).delete()

    offers_media_message = await call.message.answer_media_group(media)
    offers_message = await call.message.answer("Выберите акцию из списка", reply_markup=markup)
    await state.update_data(offers_media_message=offers_media_message)
    await state.update_data(offers_message=offers_message)
    await state.update_data(offer_page=old_page)


async def show_add_params_quest(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    offers_dict = data.get("offers_dict")
    index = value
    offer_value = offers_dict.get(index)
    offer_link = offer_value.get("link")
