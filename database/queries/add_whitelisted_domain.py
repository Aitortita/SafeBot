from database.models import Guild, WhitelistedDomain
from database import async_session
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def addWhitelistedDomain(guild_id: int, domain_name: str) -> str:
    async with async_session() as session:
        async with session.begin():
            try:
                # Query guild by id
                guild = (await session.execute(select(Guild).where(Guild.guild_id == guild_id))).scalar_one()

                if(not guild):
                   return "The guild is not stored in our databases"

                # try:
                # Check if domain exists in database  
                query = select(WhitelistedDomain).options(selectinload(WhitelistedDomain.guilds)).where(WhitelistedDomain.domain_name == domain_name)
                domain = (await session.execute(query)).scalar_one_or_none()

                if (not domain):
                    # If domain doesn't exist, create a new one
                    domain = WhitelistedDomain(domain_name=domain_name)

                if guild in list(domain.guilds):
                    return f"the domain {domain.domain_name} is already in the whitelist"
                
                # Add relationship between guild and domain
                domain.guilds.append(guild)
                    
                session.add(domain)
                await session.commit()

                return f"The domain '{domain.domain_name}' was added successfully to your whitelisted domains, this means we will now ignore this domain with our automatic scans"
            except Exception as error:
                await session.rollback()
                print(error)
            finally:
                await session.close()