import asyncio
import os
from aiogram.types import FSInputFile
from models.databases import Session
from models.dbs.models import *
from bot import bot
from config import *
from handlers.markups import *

from sqlalchemy import insert, inspect, or_, select, text
from sqlalchemy.orm import selectinload


class Orm:
    
    @staticmethod
    async def get_photo_by_filename(filename):
        async with Session() as session:
            query = select(Photo).where(Photo.photo_filename == filename)
            photo = (await session.execute(query)).scalar_one_or_none()
            return photo
    
    @staticmethod
    async def get_photo_by_id(photo_id):
        async with Session() as session:
            query = select(Photo).where(Photo.id == photo_id)
            photo = (await session.execute(query)).scalar_one_or_none()
            return photo
    
    @staticmethod
    async def create_photo(filename: str):
        async with Session() as session:
            if (await Orm.get_photo_by_filename(filename)) is not None:
                return
            query = select(PhotoSession).where(PhotoSession.end_time == None)
            photo_session = (await session.execute(query)).scalars().all()[-1]
            photo = Photo(
                session_id=photo_session.id,
                photo_filename=filename
            )
            session.add(photo)
            await session.commit()
            await session.refresh(photo)
            photo_path = await get_photo_path_by_filename(filename)
            # до этого момента все работает
            # строка ниже просто не выполняется и ничего не выводит
            await bot.send_photo(
                chat_id=photo_session.user.telegram_id,
                photo=FSInputFile(photo_path),
                caption="Фото добавлено в сессию.",
                reply_markup=await generate_raw_photo_markup(photo.id)
            )
    
    @staticmethod
    async def end_session():
        async with Session() as session:
            query = select(PhotoSession).where(PhotoSession.end_time == None)
            photo_session = (await session.execute(query)).scalars().all()[-1]
            photo_session.end_time = datetime.datetime.now()
            await session.commit()
            await session.refresh(photo_session)
            user = photo_session.user
            return user
    
    @staticmethod
    async def get_admin():
        async with Session() as session:
            query = select(User).where(User.admin == True)
            admin = (await session.execute(query)).scalar_one_or_none()
            return admin
        
    @staticmethod
    async def end_session_after_one_hour(photo_session_id):
        await asyncio.sleep(60*60)
        async with Session() as session:
            query = select(PhotoSession).where(PhotoSession.id == photo_session_id)
            photo_session = (await session.execute(query)).scalar_one()
            if photo_session.end_time is None:
                photo_session.end_time = datetime.datetime.now()
                await session.commit()
                await session.refresh(photo_session)
                await bot.send_message(
                    chat_id=photo_session.user.telegram_id,
                    text=end_session_one_hour_text,
                )
                await bot.send_message(
                    chat_id=(await Orm.get_admin()).telegram_id,
                    text=f"Сессия пользователя {photo_session.user_fio} завершена по истечении часа."
                )
    
    @staticmethod
    async def start_new_session(user):
        async with Session() as session:
            photo_session = PhotoSession(
                user_id=user.id,
                user_fio=user.fio
            )
            session.add(photo_session)
            await session.commit()
            await session.refresh(photo_session)
            asyncio.create_task(Orm.end_session_after_one_hour(photo_session.id))
    
    @classmethod
    async def create_user(cls, message, fio, phone_number):
        if await cls.get_user_by_telegram_id(message.from_user.id) is None:
            user = User(
                full_name=message.from_user.full_name,
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                fio=fio,
                phone_number=phone_number
            )
            await cls.save_user(user)
            return True
        return False
    
    @staticmethod
    async def save_user(user):
        async with Session() as session:
            await session.merge(user)
            await session.commit()
    
    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        async with Session() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            user = (await session.execute(query)).scalar_one_or_none()
            return user
    
    @staticmethod
    async def get_all_users():
        async with Session() as session:
            query = select(User)
            users = (await session.execute(query)).scalars().all()
            return users
        