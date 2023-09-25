from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine('sqlite+aiosqlite:///db.sqlite3')
SessionLocal = async_sessionmaker(bind=engine)
Base = declarative_base()

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
