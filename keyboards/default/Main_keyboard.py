from aiogram.types import KeyboardButton, InlineKeyboardMarkup

main_keyboard = InlineKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Выбор города"), KeyboardButton(text="Случайный квест")],
    [KeyboardButton(text="Выбор по фильтрам"), KeyboardButton(text="")],
    [KeyboardButton(text="")],
    [KeyboardButton(text="")],
], resize_keyboard=True)
