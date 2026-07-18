import os
import sys

from dependencias import pegar_sessao
from services.pokemon_service import (
    atualizar_pokemon,
    criar_pokemon,
    deletar_pokemon,
    listar_pokemon,
)

COR_VERDE = '\033[32m'
COR_AMARELA = '\033[33m'
COR_VERMELHA = '\033[31m'
COR_AZUL = '\033[34m'
COR_ROXA = '\033[35m'
LIMPA_COR = '\033[m'


def converter_para_int(texto: str) -> int:
    texto_convertido = int(texto)

    return texto_convertido


def converter_para_float(texto: str) -> float:
    texto_convertido = float(texto)

    return texto_convertido


async def usuario_criar_pokemon() -> str:

    dados_pokemon = {
        'nome': '',
        'altura': '',
        'peso': '',
        'experiencia_base': '',
        'tipo': '',
        'habilidade': '',
        'movimento': '',
    }

    print('\nPreencha os campos para criar o pokemon')

    for campo in dados_pokemon.keys():
        resposta_usuario = input(f'{campo.capitalize()}: ')

        dados_pokemon[campo] = resposta_usuario

    dados_pokemon['altura'] = converter_para_float(texto=dados_pokemon['altura'])

    dados_pokemon['peso'] = converter_para_float(texto=dados_pokemon['peso'])

    dados_pokemon['experiencia_base'] = converter_para_int(
        texto=dados_pokemon['experiencia_base']
    )

    async for sessao in pegar_sessao():
        dict_resposta = await criar_pokemon(
            dados_pokemon=dados_pokemon,
            sessao=sessao,
        )

        return f"\n{COR_VERDE}{dict_resposta['mensagem']}{LIMPA_COR}"


async def usuario_listar_pokemon() -> str:

    print('\nDigite o nome do pokemon que deseja buscar')

    nome_pokemon = input('\nNome: ')

    async for sessao in pegar_sessao():
        dict_resposta = await listar_pokemon(
            nome_pokemon=nome_pokemon,
            sessao=sessao,
        )

        if dict_resposta['banco'] is None and dict_resposta['api'] is None:
            print(f'{COR_AMARELA}Nenhum pokemon foi encontrado{LIMPA_COR}')
            return ''

        if dict_resposta['banco'] is None:
            print(f'\n{COR_VERDE}Pokemon encontrado com sucesso{LIMPA_COR}')

            for campo, valor in dict_resposta['api'].items():
                print(f'\n{campo}: {valor}')
            return ''
        elif dict_resposta['api'] is None:
            print(f'\n{COR_VERDE}Pokemon encontrado com sucesso{LIMPA_COR}')

            pokemon = {
                'Número do registo': dict_resposta['banco'].id,
                'Nome': dict_resposta['banco'].nome,
                'Altura': dict_resposta['banco'].altura,
                'Peso': dict_resposta['banco'].peso,
                'Experiencia base': dict_resposta['banco'].experiencia_base,
                'Tipo': dict_resposta['banco'].tipo,
                'Habilidade': dict_resposta['banco'].habilidade,
                'Movimento': dict_resposta['banco'].movimento,
            }

            for campo, valor in pokemon.items():
                print(f'\n{campo}: {valor}')
            return ''

        else:
            print(f'\n{COR_VERDE}Pokemons encontrados com sucesso{LIMPA_COR}')

            print(f'\n{COR_AZUL}Pokemon criado por fã{LIMPA_COR}')

            pokemon = {
                'Número do registo': dict_resposta['banco'].id,
                'Nome': dict_resposta['banco'].nome,
                'Altura': dict_resposta['banco'].altura,
                'Peso': dict_resposta['banco'].peso,
                'Experiencia base': dict_resposta['banco'].experiencia_base,
                'Tipo': dict_resposta['banco'].tipo,
                'Habilidade': dict_resposta['banco'].habilidade,
                'Movimento': dict_resposta['banco'].movimento,
            }

            for campo, valor in pokemon.items():
                print(f'\n{campo}: {valor}')

            print(
                f'\n{COR_ROXA}Pokemon original da{LIMPA_COR} {COR_VERMELHA}POKEDEX{LIMPA_COR}'
            )

            for campo, valor in dict_resposta['api'].items():
                print(f'\n{campo}: {valor}')
            return ''


async def usuario_atualizar_pokemon() -> str:
    print(
        f'\nDigite o {COR_AMARELA}Número do registro{LIMPA_COR} do pokemon que deseja atualizar'
    )

    numero_registro = int(input('\nNúmero do registro: '))

    print('\nPreencha os campos para atualizar o pokemon')

    dados_pokemon = {
        'nome': '',
        'altura': '',
        'peso': '',
        'experiencia_base': '',
        'tipo': '',
        'habilidade': '',
        'movimento': '',
    }

    for campo in dados_pokemon.keys():
        resposta_usuario = input(f'{campo.capitalize()}: ')

        dados_pokemon[campo] = resposta_usuario

    dados_pokemon['altura'] = converter_para_float(texto=dados_pokemon['altura'])
    dados_pokemon['peso'] = converter_para_float(texto=dados_pokemon['peso'])
    dados_pokemon['experiencia_base'] = converter_para_int(
        texto=dados_pokemon['experiencia_base']
    )

    async for sessao in pegar_sessao():
        dict_resposta = await atualizar_pokemon(
            id_pokemon=numero_registro,
            dados_pokemon=dados_pokemon,
            sessao=sessao,
        )

    return f"\n{COR_VERDE}{dict_resposta['mensagem']}{LIMPA_COR}"


async def usuario_deletar_pokemon() -> str:

    dados_pokemon = {
        'numero': '',
        'nome': '',
    }

    print(
        f'\nDigite o {COR_AMARELA}Número do registro{LIMPA_COR} '
        f'e o {COR_AMARELA}Nome{LIMPA_COR} do pokemon que deseja deletar'
    )

    for campo in dados_pokemon.keys():
        resposta_usuario = input(f'\n{campo.capitalize()}: ')

        dados_pokemon[campo] = resposta_usuario

    dados_pokemon['numero'] = converter_para_int(texto=dados_pokemon['numero'])

    async for sessao in pegar_sessao():
        dict_resposta = await deletar_pokemon(
            id_pokemon=dados_pokemon['numero'],
            nome_pokemon=dados_pokemon['nome'],
            sessao=sessao,
        )

    return f"\n{COR_VERDE}{dict_resposta['mensagem']}{LIMPA_COR}"


async def verificar_numero_usuario(numero: int) -> str:

    try:
        if numero == 0:
            sys.exit()
        elif numero == 1:
            return await usuario_criar_pokemon()
        elif numero == 2:
            return await usuario_listar_pokemon()
        elif numero == 3:
            return await usuario_atualizar_pokemon()
        elif numero == 4:
            return await usuario_deletar_pokemon()
        else:
            return f'\n{COR_VERMELHA}Número inválido, tente novamente{LIMPA_COR}'

    except Exception:
        return f'\n{COR_VERMELHA}Ocorreu um erro, tente novamente{LIMPA_COR}'
