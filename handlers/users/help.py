from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

from data import HELP_TEXT, HELP_BUTTON


@dp.message_handler(CommandHelp() | Text(HELP_BUTTON))
async def bot_help(message: types.Message):
    await message.answer(HELP_TEXT)
    from utils.universal_function import get_info_person_logging
    print(get_info_person_logging(message, "help"))
