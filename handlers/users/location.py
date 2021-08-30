from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from data import CITY_TAKE, CITY_ERROR, FILTER_QUESTS_POSTFIX, NOW_CHECK_LOCATION, GET_CITY_BUTTON, \
    FILTER_MEDIA_MESSAGE, FILTER_MESSAGE, PRETTY_CITY_NAME, cancel_command, OFFERS_MESSAGE, OFFERS_MEDIA_MESSAGE
from states import CityState
from utils.parse import get_links_soup
from utils.universal_function import error_func
from .filter import delete_category_messages
from .start import update_data_user

from loader import dp


@dp.message_handler(Command('get_location'))
async def out_location(message: Message, state: FSMContext):
    from utils.universal_function import get_info_person_logging
    print(get_info_person_logging(message, "get_location"))
    try:
        data = await state.get_data()
        if len(data) == 0 or data.get(PRETTY_CITY_NAME) is None:
            await update_data_user(state)
            data = await state.get_data()
        line = NOW_CHECK_LOCATION.format(data.get(PRETTY_CITY_NAME))
        await message.answer(line)
    except Exception as e:
        print("ERROR:", message.date, message.from_user, e, "out_location")


@dp.message_handler(Command('location') | Text(GET_CITY_BUTTON))
async def get_location_information(message: Message, state: FSMContext):
    try:
        await message.answer(CITY_TAKE)
        await CityState.Get_City.set()
        soup, pretty_cities_dict = get_links_soup()
        await state.update_data(soup=soup, pretty_cities_dict=pretty_cities_dict)
    except Exception as e:
        print("ERROR:", message.date, message.from_user, e, "get_location_information")


@dp.message_handler(state=CityState.Get_City)
async def get_city(message: Message, state: FSMContext):
    try:

        data = await state.get_data()
        soup = data.get("soup")
        pretty_cities_dict = data.get("pretty_cities_dict")
        city = message.text.lower().replace(' ', '-').replace('-', '')

        if city == cancel_command:
            await state.reset_state(with_data=False)
            await out_location(message, state)
        elif city in soup:
            main_city_link = soup[city]
            pretty_city_name = pretty_cities_dict.get(city)
            await state.update_data(city=message.text, main_city_link=main_city_link)
            await state.update_data(filtered_link=main_city_link + FILTER_QUESTS_POSTFIX)
            await state.update_data(pretty_city_name=pretty_city_name)
            await state.update_data(now_params_quest_filter=None, quest_dict=None)

            await state.update_data(pretty_cities_dict=None, soup=None)

            line = NOW_CHECK_LOCATION.format(pretty_city_name)
            await message.answer(line)

            await state.reset_state(with_data=False)
            await delete_category_messages(data, FILTER_MESSAGE, FILTER_MEDIA_MESSAGE)
            await delete_category_messages(data, OFFERS_MESSAGE, OFFERS_MEDIA_MESSAGE)
            from utils.universal_function import get_info_person_logging
            print(get_info_person_logging(message, "get_city"))

        else:
            await message.answer(CITY_ERROR)
            await CityState.Get_City.set()

    except Exception as e:
        await error_func(message, state)
        print("ERROR:", message.date, message.from_user, e, "get_city")

