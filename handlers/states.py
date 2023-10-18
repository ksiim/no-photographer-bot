from aiogram.fsm.state import State, StatesGroup


class ChangeState(StatesGroup):
    about_me_photo = State()
    
class PaymentState(StatesGroup):
    get_fio = State()
    
class ReviewState(StatesGroup):
    name = State()
    photo = State()