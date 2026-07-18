from sqlalchemy import Column, Float, Integer, String

from core.configuracoes import Base


# Define como a tabela do banco será
class Pokemon(Base):
    # Define o nome da tabela
    __tablename__ = 'pokemons'

    # Define como cada campo da tabela será
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    altura = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    experiencia_base = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    habilidade = Column(String, nullable=False)
    movimento = Column(String, nullable=False)
