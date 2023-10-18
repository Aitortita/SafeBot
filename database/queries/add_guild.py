from database.models import Guild, WhitelistedDomain
from database import async_session, domainList
from sqlalchemy import select

async def addGuild(guild_id):
    async with async_session() as session:
        async with session.begin():
            try:
                # Create new guild
                guild = Guild(guild_id=guild_id)

                # Get all BaseWhitelistedDomains from the WhitelistedDomain table
                base_whitelisted_domains = await session.execute(select(WhitelistedDomain).where(WhitelistedDomain.domain_name.in_(domainList)))

                # Associate WhitelistedDomains with the Guild
                guild.whitelisted_domains.extend(base_whitelisted_domains.scalars().all())
                
                # Add the guild to the session and commit
                session.add(guild)
                await session.commit()

                return f"Guild {guild_id} added successfully."
            except Exception as error:
                await session.rollback()
                print(error)
            finally:
                await session.close()