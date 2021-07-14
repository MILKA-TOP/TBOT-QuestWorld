from aiogram.dispatcher.filters.state import State, StatesGroup


class User_Location(StatesGroup):
    Get_Country = State()
    Get_City = State()
