import asyncio
import os

from bot import dp, bot

import logging

import handlers

from models.databases import create_database

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# add logging
logging.basicConfig(level=logging.INFO)


async def main():
    create_database()
    await dp.start_polling(bot)
    
    


if __name__ == "__main__":
    asyncio.run(main())