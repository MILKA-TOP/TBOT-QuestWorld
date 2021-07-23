from aiogram.dispatcher.filters.state import State, StatesGroup


class TBot_States(StatesGroup):
    Get_Country = State()
    Get_City = State()

    Main_Filter = State()
    Sort_Filter = State()
