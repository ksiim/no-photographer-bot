from sqlalchemy import Column, Integer, Text

from models.databases import Base, Session


class Сode(Base):
    __tablename__ = 'codes'

    id = Column(Integer, primary_key=True)
    code = Column(Text)
    
    def __init__(self, code: str):
        self.code = code
        
    def save(self):
        session = Session()
        session.merge(self)
        session.commit()
        session.close()
        
    @classmethod
    def is_code_exists(cls, code: str):
        session = Session()
        code = session.query(cls).filter(cls.code == code).first()
        session.close()
        return code is not None
        
    def delete(self):
        session = Session()
        session.delete(self)
        session.commit()
        session.close()
