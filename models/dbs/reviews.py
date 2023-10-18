from sqlalchemy import Column, Float, ForeignKey, Integer, PickleType, Text, Boolean, DateTime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from models.databases import Base, Session


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    photo = Column(Text)
    
    def __init__(self, name: str, photo: str):
        self.name = name
        self.photo = photo

        
    def save(self):
        session = Session()
        
        session.merge(self)
        
        session.commit()
        
    @classmethod
    def get_all_reviews(cls):
        session = Session()
        
        reviews = session.query(cls).all()
        
        return reviews
    
    @classmethod
    def get_by_name(cls, name: str):
        session = Session()
        
        review = session.query(cls).filter(cls.name == name).first()
        
        return review
        
    def delete(self):
        session = Session()
        
        session.delete(self)
        session.commit()
