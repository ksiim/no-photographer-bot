from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from bot import dp, bot
from config import *

import logging

import handlers

from handlers.parser import PhotoWatcher
from models.databases import create_database


logging.basicConfig(level=logging.INFO)

async def main():
    watcher = PhotoWatcher(directory=directory)
    watcher_task = asyncio.create_task(watcher.start())
    # try:
    await asyncio.gather(
        create_database(),
        dp.start_polling(bot)
    )
    # except asyncio.CancelledError:
    #     logging.info("Main task was cancelled")
    # finally:
    # watcher_task.cancel()
    # await watcher_task
    # await watcher.start()
    # await create_database()
    # await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())