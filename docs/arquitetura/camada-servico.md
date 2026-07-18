# Camada de serviço

O módulo `services/pokemon_service.py` concentra toda a regra de negócio da aplicação. Cada função corresponde a uma operação de CRUD e é independente da camada de CLI — poderia, em tese, ser reaproveitada por uma API REST sem nenhuma alteração.

## `criar_pokemon`

Recebe um dicionário de dados brutos, valida com `CriarPokemon`, cria a instância do model `Pokemon` e persiste no banco.

```python
async def criar_pokemon(dados_pokemon: dict, sessao: AsyncSession) -> dict:
```

- Valida os dados de entrada via Pydantic antes de tocar no banco.
- Em caso de falha durante o commit, desfaz a transação (`rollback`) e propaga o erro.
- Retorna uma mensagem de sucesso junto com o objeto persistido.

## `listar_pokemon`

A função mais elaborada do serviço: busca o mesmo Pokémon em **duas fontes independentes**.

```python
async def listar_pokemon(nome_pokemon: str, sessao: AsyncSession) -> dict:
```

1. Valida o nome recebido via `NomePokemon`.
2. Consulta o banco local por nome exato.
3. Faz uma requisição assíncrona à PokeAPI (`httpx.AsyncClient`, aberto e fechado automaticamente via `async with`).
4. Se a API responder com sucesso, monta um dicionário com os campos relevantes (`nome`, `altura`, `peso`, `experiencia_base`, `tipo`, `habilidade`, `movimento`) e traduz apenas os campos textuais para português usando `deep_translator`, preservando os valores numéricos como estão.
5. Retorna ambos os resultados (`banco` e `api`) — quem decide o que exibir é a camada de CLI.

Separar a consulta ao banco da consulta à API dentro da mesma função (em vez de fazer isso na camada de CLI) mantém a lógica de integração externa isolada num único lugar, mais fácil de testar com mocks.

## `atualizar_pokemon`

```python
async def atualizar_pokemon(id_pokemon: int, dados_pokemon: dict, sessao: AsyncSession) -> dict:
```

- Valida os novos dados via `AtualizarPokemon`.
- Busca o registro pelo `id`; se não existir, levanta uma exceção tratada.
- Aplica os campos validados no objeto existente com `setattr`, campo a campo.
- Segue o mesmo padrão de `commit`/`rollback` das demais operações de escrita.

## `deletar_pokemon`

```python
async def deletar_pokemon(id_pokemon: int, nome_pokemon: str, sessao: AsyncSession) -> dict:
```

- Exige **id e nome** simultaneamente como critério de exclusão — uma camada extra de segurança contra deletar o registro errado.
- Se o registro não existir ou o nome não bater com o `id` informado, levanta uma exceção.
- Após a exclusão, o commit também é protegido por `rollback` em caso de falha.

## Convenções seguidas por todas as funções

- Recebem a `AsyncSession` já pronta (via injeção, nunca criam sessão própria).
- Validam dados **antes** de qualquer escrita no banco.
- Retornam sempre um dicionário com uma mensagem e, quando aplicável, o objeto envolvido.
- Erros de negócio (registro não encontrado, dados inválidos) são sinalizados via exceção, não via valor de retorno mágico (tipo `None` ou `False`).
