import asyncio

from models.databases import Base, async_session

from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    full_name: Mapped[str]
    username: Mapped[str]
    
    async def save(self):
        async with async_session() as session:
            await session.merge(self)
            
            await session.commit()
    
    @classmethod
    async def get_user(cls, telegram_id):
        async with async_session() as session:
            stmt = select(cls).where(cls.telegram_id == telegram_id)
            
            user = await session.execute(stmt)
            
            return user.scalars().first()
            
    @classmethod
    async def get_all_users(cls):
        async with async_session() as session:
            stmt = select(cls)
            
            users = await session.execute(stmt)
            
            return users.scalars().all()
        
    async def delete(self):
        async with async_session() as session:
            
            await session.delete(self)
            
            await session.commit()
            
