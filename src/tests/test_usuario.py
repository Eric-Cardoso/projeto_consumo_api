import unittest
from unittest.mock import ANY, AsyncMock, patch

from services.usuario_service import (
    usuario_atualizar_pokemon,
    usuario_criar_pokemon,
    usuario_deletar_pokemon,
    usuario_listar_pokemon,
    verificar_numero_usuario,
)


def dados_pokemon() -> dict:
    dados_pokemon = {
        'nome': 'sombra escura',
        'altura': 1.60,
        'peso': 55.73,
        'experiencia_base': 135,
        'tipo': 'dark',
        'habilidade': 'bola sombria',
        'movimento': 'deslize das sombras',
    }

    return dados_pokemon


async def pegar_sessao_fake():
    yield AsyncMock()


class TestUsuario(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.pokemon = dados_pokemon()

    @patch('services.usuario_service.usuario_criar_pokemon')
    async def test_verificar_numero_usuario_deve_chamar_usuario_criar_pokemon(
        self,
        mock_usuario_criar_pokemon,
    ) -> None:

        # Arrange
        numero = 1

        # Act
        await verificar_numero_usuario(
            numero=numero,
        )

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_usuario_criar_pokemon.assert_awaited_once()

    @patch('services.usuario_service.criar_pokemon')
    @patch('services.usuario_service.input')
    @patch('services.usuario_service.pegar_sessao')
    @patch('services.usuario_service.converter_para_float')
    @patch('services.usuario_service.converter_para_int')
    async def test_usuario_criar_pokemon_deve_chamar_criar_pokemon(
        self,
        mock_converter_para_int,
        mock_converter_para_float,
        mock_pegar_sessao,
        mock_input,
        mock_criar_pokemon,
    ) -> None:

        # Arrange
        mock_input.side_effect = [
            'sombra escura',
            '1.60',
            '1.60',
            '135',
            'dark',
            'bola sombria',
            'deslize das sombras',
        ]

        mock_converter_para_float.return_value = 1.60

        mock_converter_para_int.return_value = 100

        mock_pegar_sessao.return_value = pegar_sessao_fake()

        # Act
        await usuario_criar_pokemon()

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_criar_pokemon.assert_awaited_once()
        mock_criar_pokemon.assert_awaited_once_with(
            dados_pokemon={
                'nome': 'sombra escura',
                'altura': 1.60,
                'peso': 1.60,
                'experiencia_base': 100,
                'tipo': 'dark',
                'habilidade': 'bola sombria',
                'movimento': 'deslize das sombras',
            },
            sessao=ANY,
        )

    @patch('services.usuario_service.usuario_listar_pokemon')
    async def test_verificar_numero_usuario_deve_chamar_usuario_listar_pokemon(
        self,
        mock_usuario_listar_pokemon,
    ) -> None:

        # Arrange
        numero = 2

        # Act
        await verificar_numero_usuario(
            numero=numero,
        )

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_usuario_listar_pokemon.assert_awaited_once()

    @patch('services.usuario_service.listar_pokemon')
    @patch('services.usuario_service.input')
    @patch('services.usuario_service.pegar_sessao')
    async def test_usuario_listar_pokemon_deve_chamar_listar_pokemon(
        self,
        mock_pegar_sessao,
        mock_input,
        mock_listar_pokemon,
    ) -> None:

        # Arrange
        mock_input.return_value = self.pokemon['nome']

        mock_pegar_sessao.return_value = pegar_sessao_fake()

        # Act
        await usuario_listar_pokemon()

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_listar_pokemon.assert_awaited_once()

    @patch('services.usuario_service.usuario_atualizar_pokemon')
    async def test_verificar_numero_usuario_deve_chamar_usuario_atualizar_pokemon(
        self,
        mock_usuario_atualizar_pokemon,
    ) -> None:

        # Arrange
        numero = 3

        # Act
        await verificar_numero_usuario(
            numero=numero,
        )

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_usuario_atualizar_pokemon.assert_awaited_once()

    @patch('services.usuario_service.atualizar_pokemon')
    @patch('services.usuario_service.input')
    @patch('services.usuario_service.pegar_sessao')
    @patch('services.usuario_service.converter_para_float')
    @patch('services.usuario_service.converter_para_int')
    async def test_usuario_atualizar_pokemon_deve_chamar_atualizar_pokemon(
        self,
        mock_converter_para_int,
        mock_converter_para_float,
        mock_pegar_sessao,
        mock_input,
        mock_atualizar_pokemon,
    ) -> None:

        # Arrange
        mock_input.side_effect = [
            2,
            'sombra escura',
            '1.60',
            '1.60',
            '135',
            'dark',
            'bola sombria',
            'deslize das sombras',
        ]

        mock_converter_para_float.return_value = 1.60

        mock_converter_para_int.return_value = 135

        mock_pegar_sessao.return_value = pegar_sessao_fake()

        # Act
        await usuario_atualizar_pokemon()

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_atualizar_pokemon.assert_awaited_once()
        mock_atualizar_pokemon.assert_awaited_once_with(
            id_pokemon=2,
            dados_pokemon={
                'nome': 'sombra escura',
                'altura': 1.60,
                'peso': 1.60,
                'experiencia_base': 135,
                'tipo': 'dark',
                'habilidade': 'bola sombria',
                'movimento': 'deslize das sombras',
            },
            sessao=ANY,
        )

    @patch('services.usuario_service.usuario_deletar_pokemon')
    async def test_verificar_numero_usuario_deve_chamar_usuario_deletar_pokemon(
        self,
        mock_usuario_deletar_pokemon,
    ) -> None:

        # Arrange
        numero = 4

        # Act
        await verificar_numero_usuario(
            numero=numero,
        )

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_usuario_deletar_pokemon.assert_awaited_once()

    @patch('services.usuario_service.deletar_pokemon')
    @patch('services.usuario_service.input')
    @patch('services.usuario_service.pegar_sessao')
    @patch('services.usuario_service.converter_para_int')
    async def test_usuario_deletar_pokemon_deve_chamar_deletar_pokemon(
        self,
        mock_converter_para_int,
        mock_pegar_sessao,
        mock_input,
        mock_deletar_pokemon,
    ) -> None:

        # Arrange
        mock_input.side_effect = [
            '2',
            'sombra escura',
        ]

        mock_converter_para_int.return_value = 2

        mock_pegar_sessao.return_value = pegar_sessao_fake()

        # Act
        await usuario_deletar_pokemon()

        # Assert
        # Garante que o comportamento da função ocorrá conforme esperado
        mock_deletar_pokemon.assert_awaited_once()
        mock_deletar_pokemon.assert_awaited_once_with(
            id_pokemon=2,
            nome_pokemon='sombra escura',
            sessao=ANY,
        )
