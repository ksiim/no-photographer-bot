import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from models.dbs.orm import Orm
import asyncio

class PhotoHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop

    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            asyncio.run_coroutine_threadsafe(self.process_new_file(filename), self.loop)
           
    async def process_new_file(self, filename):
        await Orm.create_photo(filename)

class PhotoWatcher:
    def __init__(self, directory):
        self.directory = directory
        self.loop = asyncio.get_event_loop()
        self.event_handler = PhotoHandler(self.loop)
        self.observer = Observer()

    async def start(self):
        self.observer.schedule(self.event_handler, self.directory, recursive=False)
        self.observer.start()

async def start():
    # try:
    while True:
        # Ваш код
        await asyncio.sleep(1)
    # except asyncio.CancelledError:
    #     # Обработка отмены задачи
    #     print("Task was cancelled")
    #     raise
