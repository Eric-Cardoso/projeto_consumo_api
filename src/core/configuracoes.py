from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite+aiosqlite:///pokemons.db'

engine = create_async_engine(url=DATABASE_URL)
Session_local = async_sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False
)
Base = declarative_base()
