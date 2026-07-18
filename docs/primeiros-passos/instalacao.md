# Instalação

## Requisitos

- Python 3.12 ou superior
- pip

## Estrutura esperada do projeto

```
projeto_consumo_api/
├── mkdocs.yml
├── docs/
├── src/
│   ├── main.py
│   ├── dependencias.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── venv/
├── pyproject.toml
├── .flake8
├── requirements.txt
└── README.md
```

Todo o código da aplicação vive dentro de `src/`. Os comandos de banco de dados, execução e testes são rodados a partir dessa pasta.

## Passo a passo

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

O `requirements.txt` já inclui todas as dependências necessárias, incluindo o próprio MkDocs — não é preciso instalar nada separadamente para visualizar esta documentação.

## Próximo passo

Com o ambiente instalado, o próximo passo é [configurar o banco de dados](configuracao-banco.md) antes de rodar o CLI pela primeira vez.
