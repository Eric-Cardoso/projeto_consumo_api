# Referência: `pokemon_service`

Referência técnica das funções expostas pelo módulo `services/pokemon_service.py`.

---

## `criar_pokemon`

```python
async def criar_pokemon(dados_pokemon: dict, sessao: AsyncSession) -> dict
```

**Parâmetros**

| Nome | Tipo | Descrição |
|---|---|---|
| `dados_pokemon` | `dict` | Dados brutos do Pokémon a ser criado. Validados internamente por `CriarPokemon`. |
| `sessao` | `AsyncSession` | Sessão assíncrona ativa, obtida via `pegar_sessao()`. |

**Retorno**

```python
{'mensagem': str, 'pokemon': Pokemon}
```

**Levanta**

- Qualquer exceção do SQLAlchemy durante o commit (após `rollback` da transação).
- `ValidationError` (Pydantic) se `dados_pokemon` não atender ao schema `CriarPokemon`.

---

## `listar_pokemon`

```python
async def listar_pokemon(nome_pokemon: str, sessao: AsyncSession) -> dict
```

**Parâmetros**

| Nome | Tipo | Descrição |
|---|---|---|
| `nome_pokemon` | `str` | Nome do Pokémon a ser buscado. Validado por `NomePokemon`. |
| `sessao` | `AsyncSession` | Sessão assíncrona ativa. |

**Retorno**

```python
{
    'banco': Pokemon | None,
    'api': dict | None,
}
```

- `banco` é `None` se não houver registro local com esse nome.
- `api` é `None` se a PokeAPI retornar status diferente de `200`.

**Levanta**

- `ValidationError` (Pydantic) se `nome_pokemon` não atender ao schema `NomePokemon`.

---

## `atualizar_pokemon`

```python
async def atualizar_pokemon(id_pokemon: int, dados_pokemon: dict, sessao: AsyncSession) -> dict
```

**Parâmetros**

| Nome | Tipo | Descrição |
|---|---|---|
| `id_pokemon` | `int` | Identificador do registro a ser atualizado. |
| `dados_pokemon` | `dict` | Novos valores dos campos. Validados por `AtualizarPokemon`. |
| `sessao` | `AsyncSession` | Sessão assíncrona ativa. |

**Retorno**

```python
{'mensagem': str, 'pokemon': Pokemon}
```

**Levanta**

- `Exception('Pokemon não encontrado')` se `id_pokemon` não existir.
- `ValidationError` (Pydantic) se `dados_pokemon` não atender ao schema `AtualizarPokemon`.

---

## `deletar_pokemon`

```python
async def deletar_pokemon(id_pokemon: int, nome_pokemon: str, sessao: AsyncSession) -> dict
```

**Parâmetros**

| Nome | Tipo | Descrição |
|---|---|---|
| `id_pokemon` | `int` | Identificador do registro a ser deletado. |
| `nome_pokemon` | `str` | Nome esperado do registro — precisa bater com o `id` informado. |
| `sessao` | `AsyncSession` | Sessão assíncrona ativa. |

**Retorno**

```python
{'mensagem': str}
```

**Levanta**

- `Exception('Pokemon não encontrado')` se o `id` não existir ou o `nome` não bater com o registro encontrado.
