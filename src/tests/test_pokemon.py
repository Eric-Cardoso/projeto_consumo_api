import unittest
from unittest.mock import AsyncMock, Mock
from services.pokemon_service import criar_pokemon

def dados_pokemon() -> dict:
    dados_pokemon = {
        'nome': 'sombra escura',
        'altura': 1.60,
        'peso': 55.73,
        'experiencia_base': 135,
        'tipo': 'dark',
        'habilidade': 'bola sombria',
        'movimento': 'deslize das sombras'
    }
    
    return dados_pokemon

class TestPokemon(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.pokemon = dados_pokemon()
        self.sessao = Mock()
        self.sessao.add = Mock()
        self.sessao.commit = AsyncMock()
        self.sessao.refresh = AsyncMock()
    
    
    async def test_criar_pokemon_deve_retornar_pokemon_criado_com_sucesso(
        self
    ) -> None:
        
        # Arrange
        
        dados_pokemon = self.pokemon      
        
        resultado_esperado = 'Pokemon criado com sucesso'

        # Act
        
        resultado = await criar_pokemon(
            dados_pokemon=dados_pokemon, 
            sessao=self.sessao
        )

        # Assert
        
        self.assertEqual(resultado['mensagem'], resultado_esperado)

        # Garante que add, commit e refresh sejam chamados uma única vez
        self.sessao.add.assert_called_once()
        self.sessao.commit.assert_awaited_once()
        self.sessao.refresh.assert_awaited_once()
    
    async def test_criar_pokemon_compara_os_dados_enviados_com_os_retornados(
        self
    ) -> None:
        
        # Arrange
        
        dados_pokemon = self.pokemon

        # Act
        
        resultado = await criar_pokemon(
            dados_pokemon=dados_pokemon, 
            sessao=self.sessao
        )

        pokemon_funcao = resultado['pokemon']

        # Assert
        
        self.assertEqual(pokemon_funcao.nome, dados_pokemon['nome'])
        self.assertAlmostEqual(pokemon_funcao.altura, dados_pokemon['altura'])
        self.assertAlmostEqual(pokemon_funcao.peso, dados_pokemon['peso'])
        self.assertEqual(
            pokemon_funcao.experiencia_base, dados_pokemon['experiencia_base']
        )
        self.assertEqual(pokemon_funcao.tipo, dados_pokemon['tipo'])
        self.assertEqual(pokemon_funcao.habilidade, dados_pokemon['habilidade'])
        self.assertEqual(pokemon_funcao.movimento, dados_pokemon['movimento'])

        self.sessao.add.assert_called_once()
        self.sessao.commit.assert_awaited_once()
        self.sessao.refresh.assert_awaited_once()
    
    async def test_criar_pokemon_levanta_excecao_se_commit_nao_executa(
        self
    ) -> None:
        
        # Arrange
        
        dados_pokemon = self.pokemon

        # Força uma exceção ao executar no commit
        self.sessao.commit = AsyncMock(
            side_effect=Exception('Erro ao executar commit')
        )

        # Act
        
        # Executa a função esperando que um exceção seja levantada
        with self.assertRaises(Exception):
            await criar_pokemon(
                dados_pokemon=dados_pokemon, 
                sessao=self.sessao
            )
            
        # Garante que add e o commit sejam chamados uma vez
        self.sessao.add.assert_called_once()
        self.sessao.commit.assert_awaited_once()
        
        # Garante que refresh não será chamado após falha no commit
        self.sessao.refresh.assert_not_called()
    
    async def test_criar_pokemon_levantar_exceção_ao_enviar_dados_inválidos(
        self
    ) -> None:
        # Arrange
        
        dados_pokemon = self.pokemon

        dados_errados = dados_pokemon.copy()

        # Simula um tipo inválido para o campo nome
        dados_errados['nome'] = True

        # Act
        
        with self.assertRaises(Exception):
            await criar_pokemon(
            dados_pokemon=dados_errados, 
            sessao=self.sessao
        )
            
        # Garante que add, commit e refresh não sejam chamados
        self.sessao.add.assert_not_called()
        self.sessao.commit.assert_not_called()
        self.sessao.refresh.assert_not_called()
    


    



    

        



