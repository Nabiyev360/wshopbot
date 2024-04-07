from aiogram.dispatcher.filters.state import State, StatesGroup


class SupportState(StatesGroup):
    waiting_message = State()