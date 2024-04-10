from sqlalchemy import insert, inspect, or_, select, text

import asyncio
from models.databases import Session
from models.dbs.models import *

class Orm:
    
    # @staticmethod
    # async def insert_all_codes(codes: list[str]):
    #     async with Session() as session:
    #         for code_value in codes:
    #             code = Code(code=code_value)
    #             session.add(code)
    #         await session.commit()
    
    @staticmethod
    async def save_user(User):
        async with Session() as session:
            await session.merge(User)
            await session.commit()
    
    @staticmethod
    async def get_user_by_telegram_id(telegram_id):
        async with Session() as session:
            user = await session.execute(select(User).where(User.telegram_id == telegram_id))
            return user.scalar_one_or_none()
    
    @staticmethod
    async def get_all_users():
        async with Session() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            return users
            
    @staticmethod
    async def is_code_exists(code):
        async with Session() as session:
            query = select(Code).where(Code.code == code)
            result = await session.execute(query)
            return result.scalar_one_or_none()
