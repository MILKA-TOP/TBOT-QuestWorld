from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from data import COUNTRY_TAKE, CITY_TAKE, COUNTRY_ERROR, CITY_ERROR, FULL_QUESTS_POSTFIX, FILTER_QUESTS_POSTFIX
from states import User_Location
from middlewares import get_soup
from .start import update_data_user

from loader import dp


@dp.message_handler(Command('get_location'))
async def out_location(message: Message, state: FSMContext):
    data = await state.get_data()
    if len(data) == 0:
        await update_data_user(state)
    data = await state.get_data()
    await message.answer(str(data))


@dp.message_handler(Command('location'))
async def get_location_information(message: Message, state: FSMContext):
    await message.answer(COUNTRY_TAKE)
    await state.update_data(soup=get_soup())
    await User_Location.Get_Country.set()


@dp.message_handler(state=User_Location.Get_Country)
async def get_country(message: Message, state: FSMContext):
    country = message.text.lower().replace(' ', '-').replace('-', '')
    data = await state.get_data()
    if country in data["soup"]:
        await state.update_data(country=country)

        await message.answer(CITY_TAKE)
        await User_Location.Get_City.set()
    else:
        await message.answer(COUNTRY_ERROR)
        await User_Location.Get_Country.set()


@dp.message_handler(state=User_Location.Get_City)
async def get_city(message: Message, state: FSMContext):
    city = message.text.lower().replace(' ', '-').replace('-', '')
    data = await state.get_data()
    country = data["country"]
    if city in data["soup"][country]:
        await state.update_data(city=message.text)
        main_city_link = data["soup"][country][city]
        await state.update_data(soup="")
        await state.update_data(main_city_link=main_city_link)
        await state.update_data(all_city_quests_link=main_city_link + FULL_QUESTS_POSTFIX)
        await state.update_data(filtered_link=main_city_link + FILTER_QUESTS_POSTFIX)
        await state.update_data(quest_dict=dict())
        await message.answer(str(await state.get_data()))
        await state.reset_state(with_data=False)
    else:
        await message.answer(CITY_ERROR)
        await User_Location.Get_City.set()
