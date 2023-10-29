from database.models import Guild, WhitelistedDomain
from database import async_session
from sqlalchemy import select
from logging import getLogger
logger = getLogger('sqlalchemy.engine')

async def getWhitelist(guild_id: int) -> list[str]:
    async with async_session() as session:
        async with session.begin():
            try:
                whitelisted_domains_query = (await session.execute(
                    select(WhitelistedDomain)
                    .join_from(Guild, Guild.whitelisted_domains)
                    .where(Guild.guild_id == guild_id)
                )).scalars().all()
                whitelisted_domains = [domain.domain_name for domain in whitelisted_domains_query]
                return whitelisted_domains
            except Exception as error:
                await session.rollback()
                logger.error(error)
            finally:
                await session.close()