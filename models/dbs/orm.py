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
    async def sended_photo(photo_id):
        async with Session() as session:
            query = (
                select(Photo)
                .where(Photo.id == photo_id)
            )
            photo = (await session.execute(query)).scalars().all()[-1]
            photo.sended = True
            session.add(photo)
            await session.commit()
        
    @staticmethod
    async def get_last_session_by_telegram_id(telegram_id):
        async with Session() as session:
            query = (
                select(PhotoSession)
                .join(PhotoSession.user)
                .where(User.telegram_id == telegram_id)
            )
            photo_session = (await session.execute(query)).scalars().all()[-1]
            return photo_session
        
    @staticmethod
    async def end_session():
        async with Session() as session:
            photo_session = await Orm.get_active_session()
            if photo_session is None:
                return
            photo_session.end_time = datetime.datetime.now()
            session.add(photo_session)
            await session.commit()
            await session.refresh(photo_session)
            return photo_session.user
    
    @staticmethod
    async def extend_session(user_id, extend_time):
        async with Session() as session:
            query = (
                select(PhotoSession)
                .join(PhotoSession.user)
                .where(User.telegram_id == user_id)
                .options(selectinload(PhotoSession.user))
            )
            photo_session = (await session.execute(query)).scalars().all()[-1]
            photo_session.end_time += datetime.timedelta(minutes=extend_time)
            await session.commit()
    
    @staticmethod
    async def get_session(telegram_id):
        async with Session() as session:
            query = select(PhotoSession).join(PhotoSession.user).where(PhotoSession.user.telegram_id == telegram_id)
            photo_session = (await session.execute(query)).scalar_one_or_none()
            return photo_session
    
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
    async def get_active_session():
        async with Session() as session:
            now = datetime.datetime.now()
            query = (
                select(PhotoSession)
                .join(PhotoSession.user)
                .where(PhotoSession.end_time > now)
                .options(selectinload(PhotoSession.user))
            )
            result = await session.execute(query)
            active_sessions = result.scalars().all()
            if len(active_sessions) == 0:
                return None
            else:
                active_session = active_sessions[-1]
            return active_session
    
    @staticmethod
    async def create_photo(filename: str):
        async with Session() as session:
            if (await Orm.get_photo_by_filename(filename)) is not None:
                return
            query = select(PhotoSession).where(PhotoSession.end_time == None)
            photo_session = await Orm.get_active_session()
            photo = Photo(
                session_id=photo_session.id,
                photo_filename=filename
            )
            session.add(photo)
            await session.commit()
            await session.refresh(photo)
            photo_path = await get_photo_path_by_filename(filename)
            await bot.send_photo(
                chat_id=photo_session.user.telegram_id,
                photo=FSInputFile(photo_path),
                caption=f"{filename}",
                reply_markup=await generate_raw_photo_markup(photo.id)
            )
    
    @staticmethod
    async def get_admin():
        async with Session() as session:
            query = select(User).where(User.admin == True)
            admin = (await session.execute(query)).scalar_one_or_none()
            return admin
        
    @staticmethod
    async def start_new_session(user):
        async with Session() as session:
            photo_session = PhotoSession(
                user_id=user.id,
                user_fio=user.fio,
                end_time=datetime.datetime.now() + datetime.timedelta(hours=1)
            )
            session.add(photo_session)
            await session.commit()
            await session.refresh(photo_session)
    
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
        