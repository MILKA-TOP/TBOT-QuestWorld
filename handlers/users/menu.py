from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from data import CLOSE_MENU_KEYBOARD_MESSAGE, OPEN_MENU_KEYBOARD_MESSAGE
from keyboards.default import main_keyboard
from loader import dp


@dp.message_handler(Command("menu"))
async def open_close_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    is_open_menu = data.get("menu_check")
    if is_open_menu is None or is_open_menu:
        is_open_menu = True
        await message.answer(CLOSE_MENU_KEYBOARD_MESSAGE, reply_markup=ReplyKeyboardRemove())
    elif not is_open_menu:
        await message.answer(OPEN_MENU_KEYBOARD_MESSAGE, reply_markup=main_keyboard)
    await state.update_data(menu_check=(not is_open_menu))

