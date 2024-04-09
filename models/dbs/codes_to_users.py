from sqlalchemy import Column, Float, ForeignKey, Integer, PickleType, Text, Boolean, DateTime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from models.databases import Base, Session


class CodeToUser(Base):
    __tablename__ = 'codes_to_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    promocodes_id = Column(ForeignKey("codes.id"), primary_key=True)
        
    def save(self):
        session = Session()
        session.merge(self)
        session.commit()
        session.close()

    def delete(self):
        session = Session()
        session.delete(self)
        session.commit()
        session.close()
