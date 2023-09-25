from bot import dp

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters.command import Command

from models.dbs.users import *


@dp.message(Command('start'))
async def start_message(msg: Message):
    user = User(telegram_id=msg.from_user.id,
                full_name=msg.from_user.full_name,
                username=msg.from_user.username)
    await user.save()
    await msg.answer(text=f'Hello, {msg.from_user.full_name}')
    