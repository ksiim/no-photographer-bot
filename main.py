import asyncio
import os

from bot import dp, bot

from aiogram.types import BotCommand

import logging

import handlers

from models.databases import create_database


# add logging
logging.basicConfig(level=logging.INFO)

async def insert_all_codes():
    from models.dbs.orm import Orm
    with open("promocodes.csv", 'r') as file:
        codes = [line.split(';')[-1].strip()[1:] for line in file]
        await Orm.insert_all_codes(codes)

async def main():
    # await insert_all_codes()
    await create_database()
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='активация бота'),
            BotCommand(command='help', description='мануал по использованию'),
            BotCommand(command='info', description='подробности акции'),
            BotCommand(command='legal', description='юридическая информация об акции')
        ]
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())