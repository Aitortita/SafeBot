from database.models import Guild, SafeDomain
from database import async_session

async def addSafeDomain(guild_id: int, domain: str) -> str:
    async with async_session() as session:
        async with session.begin():
            try:
                dominio = SafeDomain(domain_name=domain)
                session.add(dominio)
                await session.commit()
                return dominio.domain_name
            except Exception as error:
                print(error)