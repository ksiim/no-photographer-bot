from bot import dp, bot

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message, CallbackQuery,
)
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import F

from models.dbs.users import *

from .callbacks import *
from .markups import *
from .states import *

@dp.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()
    
    await create_user(message)
    await send_start_message(message.from_user.id)
    
async def send_start_message(telegram_id: int):
    await bot.send_message(
        chat_id=telegram_id,
        text=start_text
    )
    
async def create_user(message: Message):
    if User.get_by_telegram_id(message.from_user.id) is None:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        user.save()
