# Pokédex CLI

CLI assíncrona para gerenciamento de Pokémons, integrada à [PokeAPI](https://pokeapi.co/).

Permite criar, listar, atualizar e deletar registros num banco local (SQLite), combinando dados próprios com informações e traduções obtidas da API pública.

## Principais características

- **Async de ponta a ponta**: acesso ao banco via SQLAlchemy async e requisições HTTP via `httpx.AsyncClient`, sem operações bloqueantes na camada de I/O.
- **Validação com Pydantic**: todo dado que entra no sistema (criação, atualização e busca) passa por um schema antes de tocar no banco.
- **Enriquecimento de dados**: ao listar um Pokémon, o sistema busca tanto no banco local quanto na PokeAPI, traduzindo os campos textuais da API para português.
- **Migrations versionadas com Alembic**: o schema do banco é criado e evoluído via migrations, não por `create_all` manual.
- **Suíte de testes assíncrona**: cobertura via `unittest.IsolatedAsyncioTestCase`, com mocks de sessão de banco e de chamadas HTTP.

## Stack técnica

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12+ |
| Banco de dados | SQLite |
| ORM | SQLAlchemy (modo async) |
| Migrations | Alembic |
| Validação | Pydantic |
| Cliente HTTP | httpx |
| Testes | unittest (`IsolatedAsyncioTestCase`, `AsyncMock`) |
| API externa | [PokeAPI](https://pokeapi.co/) |

## Sobre este projeto

Este é um projeto de portfólio, feito para demonstrar competência em consumo de APIs, modelagem assíncrona e boas práticas de teste — não um sistema em produção. Algumas decisões de escopo foram tomadas conscientemente para manter o projeto enxuto e focado nesse objetivo.

## Por onde começar

- Quer rodar o projeto agora? Vá para [Instalação](primeiros-passos/instalacao.md).
- Quer entender como o código está organizado? Vá para [Arquitetura](arquitetura/visao-geral.md).
- Quer saber como os testes foram escritos? Vá para [Testes](testes.md).
