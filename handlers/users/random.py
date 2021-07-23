import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from data import quest_difficult, FORMAT_OUTPUT_QUEST
from handlers.users.start import update_data_user
from keyboards.inline import random_keyboard

from loader import dp
from middlewares import get_quests


@dp.message_handler(Command("random"))
async def get_random_quest(message: Message, state: FSMContext):
    data = await state.get_data()

    if len(data) == 0:
        await update_data_user(state)
    data = await state.get_data()

    quest_dict = data.get("quest_dict")
    if len(quest_dict) == 0:
        url_all_quests = data.get("all_city_quests_link")
        url_main = data.get("main_city_link")
        quest_dict = get_quests(url_all_quests, url_main)
        await state.update_data(quest_dict=quest_dict)

    quest_id = random.choice(list(quest_dict.keys()))
    quest_value = quest_dict.get(quest_id)

    line = FORMAT_OUTPUT_QUEST.format(quest_value[0], quest_value[1], quest_value[2],
                                      list(quest_difficult.keys())[int(quest_value[3]) - 1],
                                      quest_value[5], quest_value[6], quest_value[4])
    await message.answer(line, reply_markup=random_keyboard)


@dp.callback_query_handler(text="next_random")
async def update_quest(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)

    await call.message.delete_reply_markup()
    await call.message.delete()

    await get_random_quest(call.message, state)
