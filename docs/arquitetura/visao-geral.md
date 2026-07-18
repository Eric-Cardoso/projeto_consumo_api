# Visão geral da arquitetura

O projeto segue uma separação simples em camadas, sem frameworks web — é uma aplicação de linha de comando, mas organizada como se fosse o backend de uma API.

```
main.py
   │
   ▼
Camada de CLI (usuario_*)      -> coleta input, formata output
   │
   ▼
Camada de serviço (pokemon_service.py) -> regra de negócio, validação, I/O
   │
   ├──▶ Banco local (SQLAlchemy async / SQLite)
   └──▶ PokeAPI (httpx.AsyncClient)
```

## Camada de CLI

Funções como `usuario_criar_pokemon`, `usuario_listar_pokemon`, `usuario_atualizar_pokemon` e `usuario_deletar_pokemon` são responsáveis por:

- Coletar input do usuário via `input()`.
- Converter tipos primitivos (`converter_para_int`, `converter_para_float`).
- Chamar a camada de serviço correspondente.
- Formatar a resposta para exibição, incluindo cores ANSI.

Essa camada **não contém regra de negócio** — ela delega tudo para a camada de serviço e só cuida de entrada/saída.

## Injeção de sessão assíncrona

O acesso ao banco é feito através de `pegar_sessao()`, um generator assíncrono que entrega uma `AsyncSession` já pronta para uso:

```python
async for sessao in pegar_sessao():
    dict_resposta = await criar_pokemon(dados_pokemon=dados_pokemon, sessao=sessao)
```

Esse padrão (inspirado em injeção de dependência) centraliza a criação e o fechamento da sessão em um único lugar, evitando que cada função de serviço precise se preocupar em abrir/fechar conexão manualmente.

## Validação como porta de entrada

Nenhum dado bruto chega ao banco sem antes passar por um schema Pydantic (`CriarPokemon`, `AtualizarPokemon`, `NomePokemon`). Isso significa que a validação acontece **antes** de qualquer interação com o banco, evitando gravações inconsistentes.

## Tratamento de erros

Toda operação de escrita no banco (`criar_pokemon`, `atualizar_pokemon`, `deletar_pokemon`) segue o mesmo padrão:

```python
try:
    ...
    await sessao.commit()
except Exception:
    await sessao.rollback()
    raise
```

Ou seja: qualquer falha durante a operação desfaz alterações parciais com `rollback()` antes de propagar o erro adiante. Isso evita que o banco fique em um estado intermediário inconsistente caso algo dê errado no meio da operação.

Para mais detalhes sobre cada função, veja [Camada de serviço](camada-servico.md).
