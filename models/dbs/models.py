from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.databases import Base, Session

    
class CodeToUser(Base):
    __tablename__ = 'codes_to_users'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    code_id: Mapped[int] = mapped_column(ForeignKey('codes.id'), primary_key=True)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    full_name: Mapped[str]
    username: Mapped[str]
    admin: Mapped[bool] = mapped_column(default=False)
    used_codes: Mapped[list["Code"]] = relationship("Code", secondary='codes_to_users')
    
class Code(Base):
    __tablename__ = 'codes'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship("User", secondary='codes_to_users', overlaps="used_codes")

class Promocode(Base):
    __tablename__ = 'promocodes'

    id: Mapped[int] = mapped_column(primary_key=True)
    used: Mapped[bool] = mapped_column(default=False)
    barcode: Mapped[str] = mapped_column(unique=True)
    promocode: Mapped[str] = mapped_column(unique=True)