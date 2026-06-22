from core.configuracoes import Session_local

# Empresta a sessão do banco de dados sempre que necessário
async def pegar_sessao():
    async with Session_local() as sessao:
        yield sessao