from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

# Define o nome do arquivo do bano de dados
DATABASE_URL = 'sqlite+aiosqlite:///pokemons.db'

# Cria a engine
engine = create_async_engine(url=DATABASE_URL)

# Cria a sessão local
Session_local = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
# Cria o base
Base = declarative_base()
