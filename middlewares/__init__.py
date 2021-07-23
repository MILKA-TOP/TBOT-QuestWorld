from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .CheckInputLocation import get_soup
from .ParseCitySite import get_quests
from .Filter_Parse import get_filter_soup
from .Filter_Parse import get_sort_array
from .Filter_Parse import get_filter_quests_list
from .Filter_Parse import get_category_list

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
