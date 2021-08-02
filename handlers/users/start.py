from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data import FILTER_QUESTS_POSTFIX
from keyboards.default import main_keyboard

from loader import dp
from data import HELP_TEXT, START_TEXT
from utils.parse.CheckInputLocation import get_links_soup


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    try:
        await message.answer_photo(open("./data/Photo/start_preview.jpg", "rb"))
    finally:
        data = await state.get_data()
        if len(data) == 0:
            await update_data_user(state)
        await message.answer(START_TEXT + HELP_TEXT, reply_markup=main_keyboard)


async def update_data_user(state: FSMContext):
    soup, pretty_cities_dict = get_links_soup()
    main_city_link = soup['москва']
    await state.update_data(pretty_city_name=pretty_cities_dict.get('москва'))
    await state.update_data(city="москва")
    await state.update_data(main_city_link=main_city_link)
    await state.update_data(filtered_link=main_city_link + FILTER_QUESTS_POSTFIX)
    await state.update_data(quest_dict=None)
    await state.update_data(default_params_quest_filter=None)
