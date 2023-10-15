from database.models import Guild, SafeDomain, GuildSafeDomainAssociation
from database import async_session
from sqlalchemy import select

async def checkIfSafeDomain(guild_id: int, domains: list[str]) -> list[str]:
    async with async_session() as session:
        async with session.begin():
            try:
                safe_domains_query = await session.execute(
                    select(SafeDomain)
                    .join_from(Guild, Guild.safe_domains)
                    .where(Guild.guild_id == guild_id)
                )
                safe_domains = [domain.domain_name for domain in safe_domains_query.scalars().all()]
                unsafe_domains = [domain for domain in domains if domain not in safe_domains]
                return unsafe_domains
            except Exception as error:
                print(error)