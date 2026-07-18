# Pokédex CLI

CLI assíncrona para gerenciamento de Pokémons, integrada à [PokeAPI](https://pokeapi.co/).

Permite criar, listar, atualizar e deletar registros num banco local (SQLite), combinando dados próprios com informações e traduções obtidas da API pública.

Desenvolvida com SQLAlchemy async, Pydantic para validação, httpx para requisições HTTP e suíte de testes unitários com mocks assíncronos.

## Requisitos

- Python 3.12+

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd projeto_consumo_api

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Entre na pasta src (os comandos daqui pra frente rodam a partir dela)
cd src
```

## Configurando o banco de dados

Antes de rodar o CLI, aplique as migrations com Alembic para criar as tabelas:

```bash
alembic upgrade head
```

## Uso

```bash
python3 main.py  # Windows: python main.py
```

Ao rodar, um menu interativo vai te guiar pelas opções disponíveis:

| Opção | Ação |
|-------|------|
| 1 | Criar Pokémon |
| 2 | Listar Pokémon |
| 3 | Atualizar Pokémon |
| 4 | Deletar Pokémon |
| 0 | Sair |

Na criação e atualização, os dados são validados antes de irem para o banco. Na listagem, se o Pokémon buscado existir na PokeAPI, os dados oficiais (traduzidos para português) também são exibidos junto ao registro local, quando houver.

## Rodando os testes

```bash
python -m unittest discover -v
```

## Quer saber mais?

Este README cobre o básico para você rodar o projeto rapidamente. Para detalhes de arquitetura, módulos e decisões técnicas, consulte a **documentação completa** gerada com MkDocs.

Para visualizar a documentação localmente (a partir da raiz do projeto):

```bash
cd ..  # se você estiver dentro de src
mkdocs serve
```

Depois é só acessar `http://127.0.0.1:8000` no navegador. A documentação atualiza automaticamente conforme os arquivos são editados.

Se quiser gerar a versão estática (por exemplo, para hospedar em algum lugar):

```bash
mkdocs build
```

Isso vai gerar o site pronto na pasta `site/`.