from sqlalchemy import Column, Integer, Text, Boolean

from models.databases import Base, Session


class Promocodes(Base):
    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True)
    used = Column(Boolean)
    barcode = Column(Text)
    promocode = Column(Text)
    
    def __init__(self, barcode: str, promocode: str, used=False):
        self.barcode = barcode
        self.promocode = promocode
        self.used = used
        
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
