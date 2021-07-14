from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message

from data import FULL_QUESTS_POSTFIX, FILTER_QUESTS_POSTFIX
from middlewares import get_soup

from loader import dp
from data import HELP_TEXT, START_TEXT


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    try:
        await message.answer_photo(open("./data/Photo/start_preview.jpg", "rb"))
    finally:
        await message.answer(START_TEXT + HELP_TEXT)
        data = await state.get_data()
        print(len(data))
        if len(data) == 0:
            await update_data_user(state)


async def update_data_user(state: FSMContext):
    await state.update_data(soup=get_soup())
    data = await state.get_data()
    main_city_link = data["soup"]["россия"]['москва']
    await state.update_data(city="москва")
    await state.update_data(country="россия")
    await state.update_data(soup="")
    await state.update_data(main_city_link=main_city_link)
    await state.update_data(all_city_quests_link=main_city_link + FULL_QUESTS_POSTFIX)
    await state.update_data(filtered_link=main_city_link + FILTER_QUESTS_POSTFIX)
    await state.update_data(quest_dict=dict())

    await state.reset_state(with_data=False)
