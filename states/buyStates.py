from aiogram.dispatcher.filters.state import State, StatesGroup


class BuytState(StatesGroup):
    waiting_location = State()
    waiting_phone = State()