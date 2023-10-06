from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

DB_NAME = 'tg_bot.db'
DB_DIR = os.path.join(os.getcwd(), DB_NAME)

engine = create_engine(f'sqlite:///{DB_DIR}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

import os


def create_database():
    if not os.path.exists(DB_NAME):
        Base.metadata.create_all(bind=engine)
