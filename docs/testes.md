# Testes

A suíte de testes cobre a camada de serviço com foco em isolar completamente as dependências externas: banco de dados e chamadas HTTP nunca são acionados de verdade durante os testes.

## Framework e ferramentas

- **`unittest.IsolatedAsyncioTestCase`**: permite escrever testes `async def test_...` nativamente, sem precisar de bibliotecas externas como `pytest-asyncio`.
- **`unittest.mock.AsyncMock`**: usado para simular métodos assíncronos (ex: `sessao.commit()`, `sessao.scalar()`).
- **`unittest.mock.Mock` / `patch`**: usados para simular dependências síncronas e substituir objetos reais durante o teste.

## Padrão AAA (Arrange, Act, Assert)

Todos os testes seguem a mesma estrutura, deixando explícito o que é preparação, execução e verificação:

```python
async def test_criar_pokemon_sucesso(self):
    # Arrange
    dados_pokemon = {...}
    sessao_mock = AsyncMock()

    # Act
    resultado = await criar_pokemon(dados_pokemon, sessao_mock)

    # Assert
    self.assertEqual(resultado['mensagem'], 'Pokemon criado com sucesso')
```

## Fixture de dados: `dados_pokemon`

Em vez de repetir os mesmos valores em cada teste, um dicionário `dados_pokemon` é montado no `setUp` (ou no próprio teste) com todos os campos esperados pelo schema, e reaproveitado entre os casos de sucesso e falha.

## Mockando a sessão assíncrona

Como `sessao` é uma `AsyncSession` real do SQLAlchemy em produção, os testes substituem esse objeto por um `AsyncMock()`, configurando `return_value` ou `side_effect` conforme o cenário:

```python
sessao_mock.scalar = AsyncMock(return_value=None)  # simula "não encontrado"
```

A diferença entre os dois é importante: `return_value` sempre devolve o mesmo resultado; `side_effect` permite simular exceções ou sequências de retornos diferentes a cada chamada.

## Mockando `pegar_sessao`

Por ser um **generator assíncrono**, `pegar_sessao` não pode ser mockado com um `AsyncMock` comum. A abordagem usada é criar um generator assíncrono equivalente no próprio teste:

```python
async def fake_pegar_sessao():
    yield AsyncMock()
```

E então usar `patch` para substituir a dependência real por essa versão fake durante o teste.

## Rodando os testes

De dentro da pasta `src`:

```bash
python -m unittest discover -v
```

O `discover` localiza automaticamente todos os arquivos `test_*.py` do projeto, e `-v` exibe cada teste individualmente no output, facilitando identificar qual caso falhou.
