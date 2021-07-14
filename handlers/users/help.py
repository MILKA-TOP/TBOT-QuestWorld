from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

from data import HELP_TEXT


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(HELP_TEXT)
