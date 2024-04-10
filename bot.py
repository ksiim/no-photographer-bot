import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='html')

dp = Dispatcher() 
