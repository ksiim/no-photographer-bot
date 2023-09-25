from sqlalchemy import Column, Integer, String
from models.databases import Base, SessionLocal


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    full_name = Column(String)
    username = Column(String)
    
    def __init__(self, telegram_id, full_name, username):
        self.telegram_id = telegram_id
        self.full_name = full_name
        self.username = username
        
    async def save(self):
        session = SessionLocal()
        await session.merge(self)
        await session.commit()
        await session.close()
        
    async def delete(self):
        session = SessionLocal()
        await session.delete(self)
        await session.commit()

    