# CLI interativo

Com o ambiente instalado e o banco configurado, o CLI é iniciado com:

```bash
python3 main.py  # Windows: python main.py
```

Ao rodar, um menu numérico é exibido e guia o usuário até sair (opção `0`), que encerra o processo com `sys.exit()`.

| Opção | Ação |
|---|---|
| 1 | Criar Pokémon |
| 2 | Listar Pokémon |
| 3 | Atualizar Pokémon |
| 4 | Deletar Pokémon |
| 0 | Sair |

Qualquer valor fora dessa faixa retorna uma mensagem de número inválido, sem derrubar o programa — todo o fluxo de menu é envolvido por um `try/except` genérico em `verificar_numero_usuario`, que captura qualquer erro inesperado e devolve uma mensagem amigável em vez de um traceback.

## Criar Pokémon

Solicita, um a um, os campos: `nome`, `altura`, `peso`, `experiencia_base`, `tipo`, `habilidade` e `movimento`. Os campos numéricos (`altura`, `peso`, `experiencia_base`) são convertidos para `float`/`int` antes de seguir para validação via Pydantic. Se a validação passar, o registro é persistido no banco local.

## Listar Pokémon

Pede apenas o nome do Pokémon buscado e consulta **duas fontes ao mesmo tempo**:

- O banco de dados local, por nome.
- A [PokeAPI](https://pokeapi.co/), via HTTP.

O comportamento de exibição muda de acordo com o que foi encontrado:

- **Só no banco**: mostra o registro local.
- **Só na API**: mostra os dados oficiais, já traduzidos para português.
- **Nos dois**: mostra o registro local e, em seguida, os dados oficiais da API sob o rótulo "Pokemon original da POKEDEX" — deixando claro para o usuário qual dado veio de onde.
- **Em nenhum dos dois**: avisa que nenhum Pokémon foi encontrado.

## Atualizar Pokémon

Pede o número do registro (`id`) e, em seguida, todos os campos novamente (mesmo padrão de `Criar Pokémon`). Se o `id` não existir no banco, uma exceção é levantada e tratada como erro.

## Deletar Pokémon

Pede o número do registro **e** o nome do Pokémon. A exclusão só é feita se ambos baterem com o mesmo registro — uma camada extra de confirmação para evitar apagar o registro errado por engano.

## Saídas coloridas

As mensagens do CLI usam códigos ANSI para diferenciar visualmente o tipo de retorno:

| Cor | Uso |
|---|---|
| Verde | Sucesso |
| Amarela | Aviso (ex: nenhum resultado encontrado) |
| Vermelha | Erro |
| Azul / Roxa | Destaque informativo (ex: origem do dado na listagem) |
