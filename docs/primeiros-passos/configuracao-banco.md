# Configurando o banco de dados

O projeto usa **SQLite** como banco local e **Alembic** para versionar o schema. Isso significa que as tabelas não são criadas automaticamente ao rodar o CLI — elas precisam ser criadas explicitamente através de uma migration, antes do primeiro uso.

## Por que Alembic?

Em vez de gerar as tabelas diretamente a partir dos models (o que funciona, mas não deixa histórico de mudanças), o projeto usa migrations. Isso garante que qualquer alteração de schema fique registrada e seja aplicável de forma incremental e repetível.

## Aplicando as migrations

De dentro da pasta `src`:

```bash
alembic upgrade head
```

Esse comando aplica todas as migrations pendentes, na ordem, até deixar o schema do banco na versão mais recente (`head`). Na primeira execução, isso cria todas as tabelas necessárias — incluindo a tabela de Pokémons.

!!! note "Quando rodar de novo"
    Sempre que uma nova migration for adicionada ao projeto (por exemplo, um novo campo em `Pokemon`), rode `alembic upgrade head` novamente para atualizar o schema local.

## Próximo passo

Com o banco pronto, é hora de [rodar o CLI](../uso/cli.md).
