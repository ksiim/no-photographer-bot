from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    fio = State()
    contact = State()