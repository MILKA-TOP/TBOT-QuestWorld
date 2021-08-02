from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data import QUESTS_BY_FILTER_BUTTON, RANDOM_QUEST_BUTTON, HELP_BUTTON, OFFERS_BUTTON, CONTACTS_BUTTON, \
    GET_CITY_BUTTON

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=QUESTS_BY_FILTER_BUTTON)],
    [KeyboardButton(text=RANDOM_QUEST_BUTTON), KeyboardButton(text=OFFERS_BUTTON)],
    [KeyboardButton(text=GET_CITY_BUTTON), KeyboardButton(text=CONTACTS_BUTTON)],
    [KeyboardButton(text=HELP_BUTTON)]
], resize_keyboard=True)
