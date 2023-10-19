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
    scheduler = AsyncIOScheduler()
    scheduler.add_job(handlers.user.everyday_task, trigger='interval', seconds=60*60*24)
    scheduler.add_job(handlers.user.check_trial, trigger='interval', seconds=60*60*6)
    scheduler.start()
    await dp.start_polling(bot)
    
    


if __name__ == "__main__":
    asyncio.run(main())