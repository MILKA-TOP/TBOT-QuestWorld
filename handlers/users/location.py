from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from data import CITY_TAKE, COUNTRY_ERROR, CITY_ERROR, FULL_QUESTS_POSTFIX, FILTER_QUESTS_POSTFIX, \
    NOW_CHECK_LOCATION, GET_CITY_BUTTON
from states import CityState
from utils.parse.CheckInputLocation import get_links_soup
from .filter import delete_filter_mes
from .start import update_data_user

from loader import dp


@dp.message_handler(Command('get_location'))
async def out_location(message: Message, state: FSMContext):
    data = await state.get_data()
    if len(data) == 0:
        await update_data_user(state)
    data = await state.get_data()
    line = NOW_CHECK_LOCATION.format(data.get("pretty_city_name"))
    await message.answer(line)


@dp.message_handler(Command('location') | Text(GET_CITY_BUTTON))
async def get_location_information(message: Message, state: FSMContext):
    await message.answer(CITY_TAKE)
    await CityState.Get_City.set()
    soup, pretty_cities_dict = get_links_soup()
    await state.update_data(soup=soup)
    await state.update_data(pretty_cities_dict=pretty_cities_dict)


@dp.message_handler(state=CityState.Get_City)
async def get_city(message: Message, state: FSMContext):
    data = await state.get_data()
    soup = data.get("soup")
    pretty_cities_dict = data.get("pretty_cities_dict")
    city = message.text.lower().replace(' ', '-').replace('-', '')
    if city in soup:
        main_city_link = soup[city]
        pretty_city_name = pretty_cities_dict.get(city)
        await state.update_data(city=message.text)
        await state.update_data(main_city_link=main_city_link)
        await state.update_data(filtered_link=main_city_link + FILTER_QUESTS_POSTFIX)
        await state.update_data(pretty_city_name=pretty_city_name)
        await state.update_data(now_params_quest_filter=None)
        await state.update_data(quest_dict=None)

        await state.update_data(pretty_cities_dict=None)
        await state.update_data(soup=None)

        line = NOW_CHECK_LOCATION.format(pretty_city_name)
        await message.answer(line)

        await state.reset_state(with_data=False)
        await delete_filter_mes(data)

    else:
        await message.answer(CITY_ERROR)
        await CityState.Get_City.set()
