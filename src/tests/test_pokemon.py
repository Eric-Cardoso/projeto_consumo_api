import unittest
from unittest.mock import AsyncMock, Mock, patch
from services.pokemon_service import (
    criar_pokemon, 
    listar_pokemon, 
    atualizar_pokemon,
    deletar_pokemon,
    Pokemon,
)

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
        self.sessao.scalar = AsyncMock()
        self.sessao.commit = AsyncMock()
        self.sessao.refresh = AsyncMock()
        self.sessao.delete = AsyncMock()
    
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
        
        # Garante que a função propaga a exceção quando os dados forem inválidos
        with self.assertRaises(Exception):
            await criar_pokemon(
            dados_pokemon=dados_errados, 
            sessao=self.sessao
        )
            
        # Garante que add, commit e refresh não sejam chamados
        self.sessao.add.assert_not_called()
        self.sessao.commit.assert_not_called()
        self.sessao.refresh.assert_not_called()

    async def test_listar_pokemon_encontra_pokemon_do_banco_pelo_nome_enviado(
        self
    ) -> None:
        
        # Arrange 
        nome_pokemon = 'pikachu'

        resultado_esperado = 'pikachu'

        self.sessao.scalar.return_value = Pokemon(nome='pikachu')

        # Act
        resultado = await listar_pokemon(
            nome_pokemon=nome_pokemon, 
            sessao=self.sessao
        )

        pokemon_banco = resultado['banco']

        pokemon_retornado = pokemon_banco.nome

        # Assert
        self.assertEqual(pokemon_retornado, resultado_esperado)

        # Garante que scalar será chamado uma única vez
        self.sessao.scalar.assert_awaited_once()

    @patch('services.pokemon_service.httpx.AsyncClient')
    @patch('services.pokemon_service.deep_translator.GoogleTranslator')
    async def test_listar_pokemon_encontra_pokemon_da_api_pelo_nome_enviado(
        self,
        mock_tradutor,
        mock_assincrono
    ) -> None:
        
        # Arrange 
        nome_pokemon = 'pikachu'

        resultado_esperado = 'pikachu'

        status_code_esperado = 200

        resposta = Mock()

        resposta.status_code = 200

        resposta.json.return_value = {
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "base_experience": 112,
            "types": [
                {
                    "type": {
                        "name": "electric"
                    }
                }
            ],
            "abilities": [
                {
                    "ability": {
                        "name": "static"
                    },
                    "is_hidden": False,
                    "slot": 1
                },
                {
                    "ability": {
                        "name": "lightning-rod"
                    },
                    "is_hidden": True,
                    "slot": 3
                }
            ],
            "moves": [
                {
                    "move": {
                        "name": "mega-punch"
                    }
                }
            ]
        }
        
        cliente = mock_assincrono.return_value

        # Garante que AsyncClient seja instanciado no async with
        cliente_contexto = cliente.__aenter__.return_value

        # Simula o valor retornado do método get
        cliente_contexto.get = AsyncMock()

        cliente_contexto.get.return_value = resposta

        # Simula o valor retornado pelo translate
        instancia_tradutor = mock_tradutor.return_value

        instancia_tradutor.translate = Mock()

        instancia_tradutor.translate.return_value = 'pikachu'
        
        # Act
        resultado = await listar_pokemon(
            nome_pokemon=nome_pokemon, 
            sessao=self.sessao
        )

        pokemon_api = resultado['api']

        pokemon_retornado = pokemon_api['nome']

        # Assert
        self.assertEqual(pokemon_retornado, resultado_esperado)

        # Verifica que get será chamado uma única vez
        cliente_contexto.get.assert_called_once()
        # Verifica que get terá como parâmetro essa url
        cliente_contexto.get.assert_called_once_with(
            url='https://pokeapi.co/api/v2/pokemon/pikachu'
        )

    @patch('services.pokemon_service.httpx.AsyncClient')
    @patch('services.pokemon_service.deep_translator.GoogleTranslator')
    async def test_listar_pokemon_levanta_excecao_se_enviado_dados_invalidos(
        self,
        mock_tradutor,
        mock_assincrono,
    ) -> None:
        
        # Arrange
        nome_pokemon = True
        
        # Act
        # Verifica que a função propaga a exceção quando ocorre falha na validação
        with self.assertRaises(Exception):
            await listar_pokemon(
                nome_pokemon=nome_pokemon, 
                sessao=self.sessao
            )        

        # Assert
        # Verifica que a execução é interrompida após a falha na validação
        self.sessao.scalar.assert_not_awaited()
        mock_assincrono.assert_not_called()
        mock_tradutor.assert_not_called()
    
    @patch('services.pokemon_service.httpx.AsyncClient')
    @patch('services.pokemon_service.deep_translator.GoogleTranslator')
    async def test_listar_pokemon_levanta_excecao_se_scalar_falhar(
        self,
        mock_tradutor,
        mock_assincrono,
    ) -> None:
        
        # Arrange
        nome_pokemon = 'pikachu'
        
        self.sessao.scalar = AsyncMock(
            side_effect=Exception('Erro ao buscar no banco')
        )        

        # Act
        # Verifica que a função propaga a exceção quando ocorre uma falha no banco
        with self.assertRaises(Exception):
            await listar_pokemon(
                nome_pokemon=nome_pokemon, 
                sessao=self.sessao
            )        

        # Assert
        # Verifica que a execução é interrompida após a falha no banco
        mock_assincrono.assert_not_called()
        mock_tradutor.assert_not_called()

    @patch('services.pokemon_service.httpx.AsyncClient')
    @patch('services.pokemon_service.deep_translator.GoogleTranslator')
    async def test_listar_pokemon_levanta_excecao_se_requisicao_a_api_falhar(
        self,
        mock_tradutor,
        mock_assincrono,
    ) -> None:
        
        # Arrange
        nome_pokemon = 'pikachu'
        
        self.sessao.scalar.return_value = Pokemon(nome='pikachu')

        cliente = mock_assincrono.return_value

        cliente_contexto = cliente.__aenter__.return_value

        cliente_contexto.get = AsyncMock(
            side_effect=Exception('Erro ao fazer o get na API')
        )

        # Act
        # Verifica que a função propaga a exceção quando a requisição à API falha
        with self.assertRaises(Exception):
            await listar_pokemon(
                nome_pokemon=nome_pokemon, 
                sessao=self.sessao
            )        

        # Assert
        # Verifica que a execução é interrompida após a falha na requisição à API
        mock_tradutor.assert_not_called()

    @patch('services.pokemon_service.httpx.AsyncClient')
    @patch('services.pokemon_service.deep_translator.GoogleTranslator')
    async def test_listar_pokemon_levanta_excecao_se_o_tradutor_falhar(
        self,
        mock_tradutor,
        mock_assincrono
    ) -> None:
        
        # Arrange 
        nome_pokemon = 'pikachu'

        self.sessao.scalar.return_value = Pokemon(nome='pikachu')

        resposta = Mock()

        resposta.status_code = 200

        resposta.json.return_value = {
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "base_experience": 112,
            "types": [
                {
                    "type": {
                        "name": "electric"
                    }
                }
            ],
            "abilities": [
                {
                    "ability": {
                        "name": "static"
                    },
                    "is_hidden": False,
                    "slot": 1
                },
                {
                    "ability": {
                        "name": "lightning-rod"
                    },
                    "is_hidden": True,
                    "slot": 3
                }
            ],
            "moves": [
                {
                    "move": {
                        "name": "mega-punch"
                    }
                }
            ]
        }
        
        cliente = mock_assincrono.return_value

        # Garante que AsyncClient seja instanciado no async with
        cliente_contexto = cliente.__aenter__.return_value

        # Simula o valor retornado do método get
        cliente_contexto.get = AsyncMock()

        cliente_contexto.get.return_value = resposta

        # Simula uma falha durante a tradução
        instancia_tradutor = mock_tradutor.return_value

        instancia_tradutor.translate = Mock(
            side_effect=Exception('Erro ao traduzir conteúdo')
        )
        
        # Act
        # Verifica que a função propaga a exceção quando o tradutor falhar
        with self.assertRaises(Exception):
            await listar_pokemon(
                nome_pokemon=nome_pokemon,
                sessao=self.sessao
            )

        # Assert
        # Verifica que a falha ocorreu durante a tradução, e não em etapas anteriores
        self.sessao.scalar.assert_awaited_once()
        cliente_contexto.get.assert_awaited_once()
        instancia_tradutor.translate.assert_called_once()

    async def test_atualizar_pokemon_deve_retornar_o_pokemon_atualizado(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': 'greninja',
            'altura': 24.65,
            'peso': 86.87,
            'experiencia_base': 100,
            'tipo': 'água',
            'habilidade': 'ash greninja',
            'movimento': 'as dos ares',
        }

        resultado_esperado = 'Pokemon atualizado com sucesso'

        self.sessao.scalar.return_value = Pokemon(
            id=1,
            nome=dados_pokemon['nome'],
            altura=dados_pokemon['altura'],
            peso=dados_pokemon['peso'],
            experiencia_base=dados_pokemon['experiencia_base'],
            tipo=dados_pokemon['tipo'],
            habilidade=dados_pokemon['habilidade'],
            movimento=dados_pokemon['movimento'],
        )

        # Act
        resultado = await atualizar_pokemon(
            id_pokemon=id_pokemon,
            dados_pokemon=dados_pokemon,
            sessao=self.sessao,
        )

        # Assert
        self.assertEqual(resultado['mensagem'], resultado_esperado)

        # Garante que as dependências foram chamadas corretamente
        self.sessao.scalar.assert_awaited_once()
        self.sessao.commit.assert_awaited_once()
        self.sessao.refresh.assert_awaited_once()
    
    async def test_atualizar_pokemon_compara_dados_enviados_com_retornados(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': 'greninja',
            'altura': 24.65,
            'peso': 86.87,
            'experiencia_base': 100,
            'tipo': 'água',
            'habilidade': 'ash greninja',
            'movimento': 'as dos ares',
        }

        self.sessao.scalar.return_value = Pokemon(
            id=1,
            nome=dados_pokemon['nome'],
            altura=dados_pokemon['altura'],
            peso=dados_pokemon['peso'],
            experiencia_base=dados_pokemon['experiencia_base'],
            tipo=dados_pokemon['tipo'],
            habilidade=dados_pokemon['habilidade'],
            movimento=dados_pokemon['movimento'],
        )

        # Act
        resultado = await atualizar_pokemon(
            id_pokemon=id_pokemon,
            dados_pokemon=dados_pokemon,
            sessao=self.sessao,
        )

        db_pokemon = resultado['pokemon']

        # Assert
        self.assertEqual(db_pokemon.nome, dados_pokemon['nome'])
        self.assertEqual(db_pokemon.altura, dados_pokemon['altura'])
        self.assertEqual(db_pokemon.peso, dados_pokemon['peso'])
        self.assertEqual(
            db_pokemon.experiencia_base, dados_pokemon['experiencia_base']
        )
        self.assertEqual(db_pokemon.tipo, dados_pokemon['tipo'])
        self.assertEqual(db_pokemon.habilidade, dados_pokemon['habilidade'])
        self.assertEqual(db_pokemon.movimento, dados_pokemon['movimento'])

        # Garante que as dependências foram chamadas corretamente
        self.sessao.scalar.assert_awaited_once()
        self.sessao.commit.assert_awaited_once()
        self.sessao.refresh.assert_awaited_once()
    
    async def test_atualizar_pokemon_levanta_excecao_se_dados_enviados_forem_invalidos(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': True,
            'altura': 24.21,
            'peso': 87,
            'experiencia_base': 100,
            'tipo': 'água',
            'habilidade': 'ash greninja',
            'movimento': 'as dos ares',
        }

        # Act
        # Garante que a função propaga a exceção quando os dados forem inválidos
        with self.assertRaises(Exception):
            await atualizar_pokemon(
                id_pokemon=id_pokemon,
                dados_pokemon=dados_pokemon,
                sessao=self.sessao,
            )

        # Assert
        # Garante que nada seja executado após a falha na validação
        self.sessao.scalar.assert_not_awaited()
        self.sessao.commit.assert_not_awaited()
        self.sessao.refresh.assert_not_awaited()

    async def test_atualizar_pokemon_levanta_excecao_se_o_scalar_falhar(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': 'frogadir',
            'altura': 24.21,
            'peso': 87,
            'experiencia_base': 100,
            'tipo': 'água',
            'habilidade': 'ash greninja',
            'movimento': 'as dos ares',
        }

        self.sessao.scalar.side_effect = Exception(
            'Erro ao buscar dados no banco'
        )

        # Act
        # Garante que a função propaga a exceção quando o scalar falhar
        with self.assertRaises(Exception):
            await atualizar_pokemon(
                id_pokemon=id_pokemon,
                dados_pokemon=dados_pokemon,
                sessao=self.sessao,
            )

        # Assert
        # Garante que a origem do problema foi o scalar
        self.sessao.scalar.assert_awaited_once()
        
        # Garante que nada seja executado após falha ao buscar dados no banco
        self.sessao.commit.assert_not_awaited()
        self.sessao.refresh.assert_not_awaited()

    async def test_atualizar_pokemon_levanta_excecao_se_o_commit_falhar(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': 'frogadir',
            'altura': 24.21,
            'peso': 87,
            'experiencia_base': 100,
            'tipo': 'água',
            'habilidade': 'ash greninja',
            'movimento': 'as dos ares',
        }

        self.sessao.scalar.return_value = Pokemon(
            nome=dados_pokemon['nome'],
            altura=dados_pokemon['altura'],
            peso=dados_pokemon['peso'],
            experiencia_base=dados_pokemon['experiencia_base'],
            tipo=dados_pokemon['tipo'],
            habilidade=dados_pokemon['habilidade'],
            movimento=dados_pokemon['movimento'],
        )

        self.sessao.commit.side_effect = Exception(
            'Erro ao executar commit'
        )
        
        # Act
        # Garante que a função propaga a exceção quando o commit falhar
        with self.assertRaises(Exception):
            await atualizar_pokemon(
                id_pokemon=id_pokemon,
                dados_pokemon=dados_pokemon,
                sessao=self.sessao,
            )

        # Assert
        # Garante que a origem do problema foi o commit
        self.sessao.scalar.assert_awaited_once()
        self.sessao.commit.assert_awaited_once()
        
        # Garante que nada seja executado após falha no commit
        self.sessao.refresh.assert_not_awaited()

    async def test_atualizar_pokemon_levanta_excecao_se_o_refresh_falhar(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': 'frogadir',
            'altura': 24.21,
            'peso': 87,
            'experiencia_base': 100,
            'tipo': 'água',
            'habilidade': 'ash greninja',
            'movimento': 'as dos ares',
        }

        self.sessao.scalar.return_value = Pokemon(
            nome=dados_pokemon['nome'],
            altura=dados_pokemon['altura'],
            peso=dados_pokemon['peso'],
            experiencia_base=dados_pokemon['experiencia_base'],
            tipo=dados_pokemon['tipo'],
            habilidade=dados_pokemon['habilidade'],
            movimento=dados_pokemon['movimento'],
        )

        self.sessao.refresh.side_effect = Exception(
            'Erro ao executar o refresh'
        )
        
        # Act
        # Garante que a função propaga a exceção quando o refresh falhar
        with self.assertRaises(Exception):
            await atualizar_pokemon(
                id_pokemon=id_pokemon,
                dados_pokemon=dados_pokemon,
                sessao=self.sessao,
            )

        # Assert
        # Garante que a origem do problema foi o refresh
        self.sessao.scalar.assert_awaited_once()
        self.sessao.commit.assert_awaited_once()
        self.sessao.refresh.assert_awaited_once()
        
    async def test_deletar_pokemon_deve_retornar_pokemon_deletado_com_sucesso(
        self,
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        nome_pokemon = 'pikachu'

        pockemon_mockado = Pokemon(
            nome='pikachu',
            altura=25.42,
            peso=65.33,
            experiencia_base=150,
            tipo='água',
            habilidade='ash greninja',
            movimento='cortar',
        )
        
        self.sessao.scalar.return_value = pockemon_mockado 

        resultado_esperado = 'Pokemon deletado com sucesso'

        # Act
        resultado = await deletar_pokemon(
            id_pokemon=id_pokemon,
            nome_pokemon=nome_pokemon,
            sessao=self.sessao,
        )

        self.assertEqual(resultado['mensagem'], resultado_esperado)

        # Garante que a execução teve o comportamento esperado
        self.sessao.scalar.assert_awaited_once()
        self.sessao.delete.assert_awaited_once_with(pockemon_mockado)
        self.sessao.commit.assert_awaited_once()
    
    async def test_deletar_pokemon_levanta_excecao_se_dados_enviados_forem_invalidos(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        nome_pokemon = True

        # Act
        # Garante que a função propaga a exceção quando os dados forem inválidos
        with self.assertRaises(Exception):
            await deletar_pokemon(
                id_pokemon=id_pokemon,
                nome_pokemon=nome_pokemon,
                sessao=self.sessao,
            )

        # Assert
        # Garante que nada seja executado após a falha na validação
        self.sessao.scalar.assert_not_awaited()
        self.sessao.delete.assert_not_awaited()
        self.sessao.commit.assert_not_awaited()

    async def test_deletar_pokemon_levanta_excecao_se_o_scalar_falhar(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        nome_pokemon = 'venossaur'

        self.sessao.scalar.side_effect = Exception(
            'Erro ao buscar dados no banco'
        )

        # Act
        # Garante que a função propaga a exceção quando o scalar falhar
        with self.assertRaises(Exception):
            await deletar_pokemon(
                id_pokemon=id_pokemon,
                nome_pokemon=nome_pokemon,
                sessao=self.sessao,
            )

        # Assert
        # Garante que a origem do problema foi o scalar
        self.sessao.scalar.assert_awaited_once()
        
        # Garante que nada seja executado após falha ao buscar dados no banco
        self.sessao.delete.assert_not_awaited()
        self.sessao.commit.assert_not_awaited()
    
    async def test_deletar_pokemon_levanta_excecao_se_o_delete_falhar(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': 'eve',
            'altura': 24.21,
            'peso': 87,
            'experiencia_base': 100,
            'tipo': 'normal',
            'habilidade': 'dançar',
            'movimento': 'ataque rapido',
        }

        self.sessao.scalar.return_value = Pokemon(
            nome=dados_pokemon['nome'],
            altura=dados_pokemon['altura'],
            peso=dados_pokemon['peso'],
            experiencia_base=dados_pokemon['experiencia_base'],
            tipo=dados_pokemon['tipo'],
            habilidade=dados_pokemon['habilidade'],
            movimento=dados_pokemon['movimento'],
        )

        self.sessao.delete.side_effect = Exception(
            'Erro ao executar o delete'
        )
        
        # Act
        # Garante que a função propaga a exceção quando o delete falhar
        with self.assertRaises(Exception):
            await deletar_pokemon(
                id_pokemon=id_pokemon,
                nome_pokemon=dados_pokemon['nome'],
                sessao=self.sessao,
            )

        # Assert
        # Garante que a origem do problema foi o delete
        self.sessao.scalar.assert_awaited_once()
        self.sessao.delete.assert_awaited_once()

        # Garante que nada será executado após falha no delete
        self.sessao.commit.assert_not_awaited()

    async def test_deletar_pokemon_levanta_excecao_se_o_commit_falhar(
        self
    ) -> None:
        
        # Arrange
        id_pokemon = 1

        dados_pokemon = {
            'nome': 'ralucha',
            'altura': 24.21,
            'peso': 87,
            'experiencia_base': 100,
            'tipo': 'normal',
            'habilidade': 'dançar',
            'movimento': 'ataque rapido',
        }

        self.sessao.scalar.return_value = Pokemon(
            nome=dados_pokemon['nome'],
            altura=dados_pokemon['altura'],
            peso=dados_pokemon['peso'],
            experiencia_base=dados_pokemon['experiencia_base'],
            tipo=dados_pokemon['tipo'],
            habilidade=dados_pokemon['habilidade'],
            movimento=dados_pokemon['movimento'],
        )

        self.sessao.commit.side_effect = Exception(
            'Erro ao executar o commit'
        )
        
        # Act
        # Garante que a função propaga a exceção quando o commit falhar
        with self.assertRaises(Exception):
            await deletar_pokemon(
                id_pokemon=id_pokemon,
                nome_pokemon=dados_pokemon['nome'],
                sessao=self.sessao,
            )

        # Assert
        # Garante que a origem do problema foi o commit
        self.sessao.scalar.assert_awaited_once()
        self.sessao.delete.assert_awaited_once()
        self.sessao.commit.assert_awaited_once()

        



    
    



        




        




    


    



    

        



