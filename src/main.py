import asyncio

from services.usuario_service import verificar_numero_usuario

COR_VERMELHA = '\033[31m'
LIMPA_COR = '\033[m'


async def executar() -> None:
    print('=' * 20)
    print(f'Bem vindo a {COR_VERMELHA}Pokédex{LIMPA_COR}')
    print('=' * 20)

    while True:
        print(
            f'\nO que deseja?\n'
            f'0 - Sair\n'
            f'1 - Criar Pokemon\n'
            f'2 - Buscar Pokemon\n'
            f'3 - Atualizar Pokemon\n'
            f'4 - Deletar Pokemon\n'
        )

        try:
            escolha_usuario = int(input('Escolha: '))
            print(await verificar_numero_usuario(numero=escolha_usuario))
            continue

        except ValueError:
            print(f'\n{COR_VERMELHA}Número inválido, tente novamente{LIMPA_COR}')
            continue


if __name__ == '__main__':
    print(asyncio.run(executar()))
