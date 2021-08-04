from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

random_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="🎲 Новый квест", callback_data="next_random")]], resize_keyboard=True
)
