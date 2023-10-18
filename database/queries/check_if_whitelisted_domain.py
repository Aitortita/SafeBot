from database.models import Guild, WhitelistedDomain
from database import async_session
from sqlalchemy import select

async def checkIfWhitelistedDomain(guild_id: int, domains: list[str]) -> list[str]:
    async with async_session() as session:
        async with session.begin():
            try:
                whitelisted_domains_query = await session.execute(
                    select(WhitelistedDomain)
                    .join_from(Guild, Guild.whitelisted_domains)
                    .where(Guild.guild_id == guild_id)
                )
                whitelisted_domains = [domain.domain_name for domain in whitelisted_domains_query.scalars().all()]
                unwhitelisted_domains = [domain for domain in domains if domain not in whitelisted_domains]
                return unwhitelisted_domains
            except Exception as error:
                await session.rollback()
                print(error)
            finally:
                await session.close()