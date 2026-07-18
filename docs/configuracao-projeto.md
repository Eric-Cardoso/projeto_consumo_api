# Configuração do projeto

Todo o toolchain de qualidade de código está centralizado em `pyproject.toml` (para `black` e `isort`) e num arquivo `.flake8` separado (já que `flake8` não lê configuração de `pyproject.toml` nativamente).

## Ordem de execução

```
isort → black → flake8
```

A ordem importa: `isort` organiza os imports primeiro, `black` formata o restante do código (incluindo os imports já organizados), e `flake8` roda por último apenas para checar o que sobrou — ele não formata nada, só reporta problemas.

## `black`

```toml
[tool.black]
line-length = 88
skip-string-normalization = true
```

- `line-length = 88`: segue o padrão do próprio `black` (mais generoso que os 79 do PEP8 puro).
- `skip-string-normalization = true`: mantém aspas simples (`'`) como estão, em vez de forçar tudo para aspas duplas (`"`) — preferência de estilo do projeto.

## `isort`

```toml
[tool.isort]
profile = "black"
line_length = 88
```

O `profile = "black"` configura o `isort` para gerar uma saída compatível com o estilo do `black`, evitando que os dois entrem em conflito e fiquem "brigando" a cada execução.

## `flake8`

Configurado em um arquivo `.flake8` próprio na raiz do projeto, mantendo o `line-length` alinhado aos 88 caracteres do `black` — do contrário, o `flake8` reportaria como erro linhas que o `black` já considera válidas.

## Rodando o toolchain manualmente

```bash
isort .
black .
flake8 .
```

## Convenção de commits

O projeto segue [Conventional Commits](https://www.conventionalcommits.org/), mantendo o histórico do repositório organizado e legível (`feat:`, `fix:`, `docs:`, `test:`, etc.).
