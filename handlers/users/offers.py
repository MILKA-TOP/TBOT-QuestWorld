from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from data import OFFERS_BUTTON, OFFERS_QUESTS_POSTFIX, FORMAT_OUTPUT_QUEST, OFFER_DESCRIBE, \
    QUEST_TELEGRAM_PAGE_COUNT, ERROR_MESSAGE, quest_difficult_demonstrate, DIFFICULTY, OFFER_MESSAGE, MAIN_CITY_LINK, \
    loading_postfix_message, LINK, NEXT_VALUE, BACK_VALUE, \
    show_offer_list_message, zero_offers_message, TYPE_CALLBACK, VALUE, PAGE, OPEN_ADD_INFO, OPEN_QUEST, OPEN_OFFER, \
    BACK_LIST, OFFERS_MEDIA_MESSAGE, NEW_QUEST_VALUE, OFFERS_MESSAGE, OFFERS_DICT, QUEST_VALUE, OFFER_PAGE, OFFER, \
    PRETTY_CITY_NAME

from handlers.users.filter import delete_media_message
from handlers.users.start import update_data_user, bot_start
from keyboards.inline import main_universal_keyboard, quest_add_params_keyboard, offer_cd, \
    temp_back_quest_menu_inline_markup_offer, back_list_offer_button
from loader import dp
from utils.parse import get_offers_parse, get_full_offer_info
from utils.parse import get_quest_params
from utils.universal_function import show_add_quest_params, delete_category_messages, error_func


@dp.message_handler(Command("offers") | Text(OFFERS_BUTTON))
async def show_offers_city(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        main_city_link = data.get(MAIN_CITY_LINK)

        await delete_category_messages(data, OFFERS_MESSAGE, OFFERS_MEDIA_MESSAGE)

        if main_city_link is None:
            await update_data_user(state)
            data = await state.get_data()
            main_city_link = data.get(MAIN_CITY_LINK)

        offers_dict = get_offers_parse(main_city_link + OFFERS_QUESTS_POSTFIX, main_city_link)

        if len(offers_dict) == 0:
            await message.answer(zero_offers_message)
        else:
            markup, media = await main_universal_keyboard(offers_dict, 0, OFFER_DESCRIBE, OFFER)
            offers_media_message = await message.answer_media_group(media)
            offers_message = await message.answer(show_offer_list_message.format(city=data.get(PRETTY_CITY_NAME)),
                                                  reply_markup=markup)
            await state.update_data(offers_dict=offers_dict, offers_media_message=offers_media_message)
            await state.update_data(offers_message=offers_message, offer_page=0)
    except Exception as e:
        print("ERROR:", message.date, message.from_user, e, "show_offers_city")


@dp.callback_query_handler(offer_cd.filter())
async def offer_navigate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    type_callback = callback_data.get(TYPE_CALLBACK)

    value = callback_data.get(VALUE)

    level = {
        OPEN_OFFER: show_another_offer,
        OPEN_QUEST: show_quest_offer,
        PAGE: change_offer_keyboard,
        OPEN_ADD_INFO: show_add_params_quest,
        BACK_LIST: back_offer_list
    }

    function = level[type_callback]

    try:
        await function(call, state, value=value)
    except Exception as e:
        await error_func(call.message, state)
        print("ERROR:", call.message.date, call.message.from_user, e, "offer_navigate")


async def show_another_offer(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    index = int(value)

    await delete_media_message(data, OFFERS_MEDIA_MESSAGE)
    await data.get(OFFERS_MESSAGE).delete()

    loading_message = await call.message.answer(loading_postfix_message)

    offer_value = data.get(OFFERS_DICT).get(index)
    link = offer_value.get(LINK)
    offer_info_dict = get_full_offer_info(link)
    message_text = OFFER_MESSAGE.format(**offer_info_dict)
    markup = back_list_offer_button
    try:
        await loading_message.edit_text(message_text, reply_markup=markup)
    except Exception:
        await loading_message.edit_text(
            OFFER_MESSAGE.format(head=offer_info_dict.get("head"), body=offer_info_dict.get("body_text")),
            reply_markup=markup)
    await state.update_data(offers_message=loading_message)


async def show_quest_offer(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    index = int(value)
    new_quest_value = data.get(NEW_QUEST_VALUE)

    if new_quest_value is None:
        await delete_media_message(data, OFFERS_MEDIA_MESSAGE)
        await data.get(OFFERS_MESSAGE).delete()

        loading_message = await call.message.answer(loading_postfix_message)
        quest_value = data.get(OFFERS_DICT).get(index)
        link = quest_value.get(LINK)
        new_quest_value = get_quest_params(link, full_info=True)
        quest_value.update(new_quest_value)

        await state.update_data(new_quest_value=new_quest_value, quest_value=quest_value)

        markup = await quest_add_params_keyboard(quest_value, callback_type=OFFER)

        difficulty = quest_difficult_demonstrate[quest_value[DIFFICULTY] - 1]
        await loading_message.edit_text(FORMAT_OUTPUT_QUEST.format(dif_text=difficulty, **quest_value),
                                        reply_markup=markup)
        await state.update_data(offers_message=loading_message)

    else:
        quest_value = data.get(QUEST_VALUE)
        markup = await quest_add_params_keyboard(quest_value, callback_type=OFFER)

        difficulty = quest_difficult_demonstrate[quest_value[DIFFICULTY] - 1]
        quest_message = await call.message.edit_text(FORMAT_OUTPUT_QUEST.format(dif_text=difficulty, **quest_value),
                                                     reply_markup=markup)
        await state.update_data(offers_message=quest_message)


async def back_offer_list(call: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    await call.message.delete()

    if data.get(NEW_QUEST_VALUE) is not None:
        await state.update_data(new_quest_value=None)
        await state.update_data(new_quest_value=None)

    offers_dict = data.get(OFFERS_DICT)
    page_number = data.get(OFFER_PAGE)
    markup, media = await main_universal_keyboard(offers_dict, page_number * QUEST_TELEGRAM_PAGE_COUNT, OFFER_DESCRIBE,
                                                  OFFER)

    await state.update_data(offers_media_message=(await call.message.answer_media_group(media)))
    filter_message = await call.message.answer(show_offer_list_message.format(city=data.get(PRETTY_CITY_NAME)),
                                               reply_markup=markup)
    await state.update_data(offers_message=filter_message)


async def change_offer_keyboard(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    page_offer = data.get(OFFER_PAGE)
    offers_dict = data.get(OFFERS_DICT)
    if value == NEXT_VALUE:
        page_offer += 1
    elif value == BACK_VALUE:
        page_offer -= 1
    markup, media = await main_universal_keyboard(offers_dict, page_offer * QUEST_TELEGRAM_PAGE_COUNT, OFFER_DESCRIBE,
                                                  OFFER)
    await delete_media_message(data, OFFERS_MEDIA_MESSAGE)
    await (data.get(OFFERS_MESSAGE)).delete()

    offers_media_message = await call.message.answer_media_group(media)
    offers_message = await call.message.answer(show_offer_list_message.format(city=data.get(PRETTY_CITY_NAME)),
                                               reply_markup=markup)

    await state.update_data(offers_media_message=offers_media_message, offers_message=offers_message,
                            offer_page=page_offer)


async def show_add_params_quest(call: CallbackQuery, state: FSMContext, value: str):
    data = await state.get_data()
    offer_value = data.get(QUEST_VALUE)
    await show_add_quest_params(call, value, offer_value, temp_back_quest_menu_inline_markup_offer)
