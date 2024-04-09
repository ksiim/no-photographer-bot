import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='html')
bot.set_my_commands(
    [
        types.BotCommand('start', 'активация бота'),
        types.BotCommand('help', 'мануал по использованию'),
        types.BotCommand('info', 'подробности акции'),
        types.BotCommand('legal', 'юридическая информация об акции')
    ]
)

dp = Dispatcher() 
