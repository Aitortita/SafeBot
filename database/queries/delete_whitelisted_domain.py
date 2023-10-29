from database.models import Guild, WhitelistedDomain
from database import async_session
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from logging import getLogger
logger = getLogger('sqlalchemy.engine')

async def deleteWhitelistedDomain(guild_id: int, domain_name: str) -> str:
    async with async_session() as session:
        async with session.begin():
            try:
                # Query guild by id
                guild = (await session.execute(select(Guild).options(selectinload(Guild.whitelisted_domains)).where(Guild.guild_id == guild_id))).scalar_one_or_none()

                if(not guild):
                   return "The guild is not stored in our databases"

                logger.info(f"guild's whitelist: {guild.whitelisted_domains}")

                whitelist = [whitelisted_domain.domain_name for whitelisted_domain in guild.whitelisted_domains]

                # Return if domain doesn't exist
                if (domain_name not in whitelist):
                    logger.info('domain not in whitelist')
                    return f"Domain {domain_name} doesn't exist on server's whitelist"
                
                else:
                    domain = next((domain for domain in guild.whitelisted_domains if domain.domain_name == domain_name), None)
                    guild.whitelisted_domains.remove(domain)

                session.add(guild)
                await session.commit()
                return f"The domain '{domain_name}' was removed successfully from your whitelisted domains, this means we will now continue scanning this domain with our automatic scans"
            except Exception as error:
                await session.rollback()
                logger.error(error)
            finally:
                await session.close()