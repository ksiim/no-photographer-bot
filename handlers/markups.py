from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *


try_again_code_text = "Код не найден или вы его уже активировали . Попробуйте еще раз."
start_text = "Привет! Я бот, который поможет тебе активировать промокод и получить подарок. Для начала отправь мне код, который ты получил!"
help_text = "Чтобы активировать промокод, отправь /start. Если код действителен, то ты получишь подарок!"


close_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Закрыть", callback_data="close")]
    ]
)

async def get_reward_text(promocode):
    return f"Код успешно активирован!\nВот ваш промокод:\n\n{promocode}"