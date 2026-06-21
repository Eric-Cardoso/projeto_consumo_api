from sqlalchemy import Column, Integer, String, Float
from core.configuracoes import Base

class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    altura = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    experiencia_base = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    habilidade = Column(String, nullable=False)
    movimento = Column(String, nullable=False)