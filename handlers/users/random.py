import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from data import FORMAT_OUTPUT_QUEST_RANDOM, quest_difficult_demonstrate, RANDOM_QUEST_BUTTON, \
    QUEST_DICT, MAIN_CITY_LINK, PRETTY_CITY_NAME
from handlers.users.start import update_data_user
from keyboards.inline import random_keyboard

from loader import dp
from utils.parse import get_quests


@dp.message_handler(Command("random") | Text(RANDOM_QUEST_BUTTON))
async def get_random_quest(message: Message, state: FSMContext, first_send=True):
    from utils.universal_function import get_info_person_logging
    print(get_info_person_logging(message, "random"))
    try:
        data = await state.get_data()
        url_main = data.get(MAIN_CITY_LINK)

        if len(data) == 0 or url_main is None:
            await update_data_user(state)
        data = await state.get_data()

        quest_dict = data.get(QUEST_DICT)
        if first_send:
            url_main = data.get(MAIN_CITY_LINK)
            quest_dict = get_quests(url_main, url_main)
            await state.update_data(quest_dict=quest_dict)

        quest_id = random.choice(list(quest_dict.keys()))
        quest_value = quest_dict.get(quest_id)

        difficulty = quest_difficult_demonstrate[int(quest_value["difficulty"]) - 1]
        line = FORMAT_OUTPUT_QUEST_RANDOM.format(dif_text=difficulty, **quest_value, city=data.get(PRETTY_CITY_NAME))

        await message.answer(line, reply_markup=random_keyboard)
    except Exception as e:
        print("ERROR:", message.date, message.from_user, e, "get_random_quest")


@dp.callback_query_handler(text="next_random")
async def update_quest(call: CallbackQuery, state: FSMContext):
    from utils.universal_function import get_info_person_logging
    print(get_info_person_logging(call.message, "next_random"))
    try:

        await call.answer(cache_time=60)

        await call.message.delete_reply_markup()
        await call.message.delete()

        await get_random_quest(call.message, state, first_send=False)
    except Exception as e:
        print("ERROR:", call.message.date, call.message.from_user, e, "update_quest")

