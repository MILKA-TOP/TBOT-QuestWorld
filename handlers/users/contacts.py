from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message

from data import CONTACTS, CONTACTS_BUTTON
from loader import dp


@dp.message_handler(Command("contacts") | Text(CONTACTS_BUTTON))
async def show_contacts(message: Message):
    await message.answer(CONTACTS, disable_web_page_preview=True)
