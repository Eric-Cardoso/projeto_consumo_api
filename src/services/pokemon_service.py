from sqlalchemy.ext.asyncio import AsyncSession
from schemas.pokemon_schema import CriarPokemon, NomePokemon
from models.pokemon_model import Pokemon
from sqlalchemy import select
import deep_translator, httpx


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

async def listar_pokemon(nome_pokemon: str, sessao: AsyncSession) -> dict:
    nome_validado = NomePokemon(nome=nome_pokemon)
    
    url_pokemon = f'https://pokeapi.co/api/v2/pokemon/{nome_validado.nome}'
    
    db_pokemon = await sessao.scalar(
        select(Pokemon)
        .where(Pokemon.nome == nome_validado.nome)
    )

    # Garante que o cliente HTTP seja fechado automaticamente
    async with httpx.AsyncClient() as cliente:
        resposta = await cliente.get(url=url_pokemon)

    if resposta.status_code != 200:
        api_pokemon = None

    else:
        dict_resposta = resposta.json()
        
        tradutor = deep_translator.GoogleTranslator(source='en', target='pt')
        
        dict_pokemon = {
            'nome': dict_resposta['name'],
            'altura': dict_resposta['height'],
            'peso': dict_resposta['weight'],
            'experiencia_base': dict_resposta['base_experience'],
            'tipo': dict_resposta['types'][0]['type']['name'],
            'habilidade': dict_resposta['abilities'][0]['ability']['name'],
            'movimento': dict_resposta['moves'][0]['move']['name']
        }

        # Traduz apenas os campos textuais, preservando os valores numéricos
        api_pokemon = {
            chave: tradutor.translate(valor)
            if isinstance(valor, str) else valor
            for chave, valor in dict_pokemon.items()
        }

    return {
        'banco': db_pokemon,
        'api': api_pokemon,
    }
    
    