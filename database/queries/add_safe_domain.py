from database.models import Guild, SafeDomain
from database import async_session
from sqlalchemy import select

async def addSafeDomain(guild_id: int, domain: str) -> str:
    async with async_session() as session:
        async with session.begin():
            try:
                guild = (await session.execute(select(Guild).where(Guild.guild_id == guild_id))).first()
                if(not guild):
                   return "the guild is not stored in our databases"
                print(f"guild: {guild}")
                dominio = SafeDomain(domain_name=domain)
                dominio.guilds.extend(guild)
                session.add(dominio)
                await session.commit()
                return dominio.domain_name
            except Exception as error:
                print(error)