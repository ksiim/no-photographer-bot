from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship

from models.databases import Base, Session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    full_name = Column(Text)
    username = Column(Text)
    admin = Column(Boolean)
    used_codes = relationship("codes", secondary="codes_to_users")
    
    def __init__(self, telegram_id: int, full_name: str, username: str,
                 admin=False):
        self.telegram_id = telegram_id
        self.full_name = full_name
        self.username = username
        self.admin = admin
        
    def save(self):
        session = Session()
        
        session.merge(self)
        
        session.commit()
        
    def can_use_promocode(self, promocode):
        return promocode not in self.used_promocodes
        
    @classmethod
    def get_by_telegram_id(cls, telegram_id: int):
        session = Session()
        
        user = session.query(cls).filter(cls.telegram_id == telegram_id).first()
        return user
    
    @classmethod
    def get_all_users(cls):
        session = Session()
        
        users = session.query(cls).all()
        return users
    
    @classmethod
    def get_admins(cls):
        session = Session()
        
        admins = session.query(cls).filter(cls.admin == True).all()
        return admins
        
    def delete(self):
        session = Session()
        
        session.delete(self)
        session.commit()
