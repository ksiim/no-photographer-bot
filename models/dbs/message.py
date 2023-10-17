from sqlalchemy import Column, Float, ForeignKey, Integer, PickleType, Text, Boolean, DateTime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from models.databases import Base, Session


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    info = Column(Text)
    
    def __init__(self, name: str, info: str):
        self.name = name
        self.info = info
    
        
    def save(self):
        session = Session()
        
        session.merge(self)
        
        session.commit()
        
    @classmethod
    def get_by_name(cls, name: str):
        session = Session()
        
        item = session.query(cls).filter(cls.name == name).first()
        
        return item
        
    def delete(self):
        session = Session()
        
        session.delete(self)
        session.commit()
