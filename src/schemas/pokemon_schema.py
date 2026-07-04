from pydantic import BaseModel, Field
from decimal import Decimal

class CriarPokemon(BaseModel):
    nome: str = Field(min_length=3)
    altura: float
    peso: float 
    experiencia_base: int
    tipo: str = Field(min_length=3)
    habilidade: str = Field(min_length=3)
    movimento: str = Field(min_length=3)

class NomePokemon(BaseModel):
    nome: str