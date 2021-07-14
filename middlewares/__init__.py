from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .CheckInputLocation import get_soup
from .ParseCitySite import get_quests

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
