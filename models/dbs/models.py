from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.databases import Base
import datetime
    
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    full_name: Mapped[str]
    username: Mapped[str]
    admin: Mapped[bool] = mapped_column(default=False)
    fio: Mapped[str]
    phone_number: Mapped[str]
    registration_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    photo_sessions: Mapped[list["PhotoSession"]] = relationship("PhotoSession", back_populates="user")
    
class PhotoSession(Base):
    __tablename__ = 'photo_sessions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship("User", back_populates="photo_sessions")
    user_fio: Mapped[str]
    start_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    end_time: Mapped[datetime.datetime] = mapped_column(nullable=True)
    
class Photo(Base):
    __tablename__ = 'photos'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('photo_sessions.id'))
    session: Mapped[PhotoSession] = relationship(PhotoSession, lazy="joined")
    photo_filename: Mapped[str]
    add_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    sended: Mapped[bool] = mapped_column(default=False)
    