from core.configuracoes import Session_local

async def pegar_sessao():
    async with Session_local() as sessao:
        yield sessao