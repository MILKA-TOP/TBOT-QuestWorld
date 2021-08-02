import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from data import quest_difficult_filter, FORMAT_OUTPUT_QUEST_RANDOM, quest_difficult_demonstrate, RANDOM_QUEST_BUTTON
from handlers.users.start import update_data_user
from keyboards.inline import random_keyboard

from loader import dp
from utils.parse.ParseCitySite import get_quests


@dp.message_handler(Command("random") | Text(RANDOM_QUEST_BUTTON))
async def get_random_quest(message: Message, state: FSMContext, first_send=True):
    data = await state.get_data()
    url_main = data.get("main_city_link")

    if len(data) == 0 or url_main is None:
        await update_data_user(state)
    data = await state.get_data()

    quest_dict = data.get("quest_dict")
    if first_send:
        url_main = data.get("main_city_link")
        quest_dict = get_quests(url_main, url_main)
        await state.update_data(quest_dict=quest_dict)

    quest_id = random.choice(list(quest_dict.keys()))
    quest_value = quest_dict.get(quest_id)

    difficulty = quest_difficult_demonstrate[int(quest_value["difficulty"]) - 1]
    line = FORMAT_OUTPUT_QUEST_RANDOM.format(dif_text=difficulty, **quest_value)

    await message.answer(line, reply_markup=random_keyboard)


@dp.callback_query_handler(text="next_random")
async def update_quest(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    await call.message.delete_reply_markup()
    await call.message.delete()

    await get_random_quest(call.message, state, first_send=False)
