from sqlalchemy.ext.asyncio import AsyncSession
from schemas.pokemon_schema import CriarPokemon
from models.pokemon_model import Pokemon

async def criar_pokemon(dados_pokemon: dict, sessao: AsyncSession) -> dict:

    pokemon_validado = CriarPokemon(**dados_pokemon)
    
    db_pokemon = Pokemon(**pokemon_validado.model_dump())

    try:
        sessao.add(db_pokemon)

        await sessao.commit()
        
        await sessao.refresh(db_pokemon)
    except Exception:
        await sessao.rollback()
        raise

    return {
        'mensagem': 'Pokemon criado com sucesso',

        'pokemon': db_pokemon
    }