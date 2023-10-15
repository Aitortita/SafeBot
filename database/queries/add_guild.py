from database.models import Guild, SafeDomain
from database import async_session, domainList
from sqlalchemy import select

async def addGuild(guild_id):
    async with async_session() as session:
        async with session.begin():
            try:
                # Create new guild
                guild = Guild(guild_id=guild_id)

                # Get all AbsoluteSafeDomains from the SafeDomain table
                absolute_safe_domains = await session.execute(select(SafeDomain).where(SafeDomain.domain_name.in_(domainList)))

                # Associate SafeDomains with the Guild
                guild.safe_domains.extend(absolute_safe_domains.scalars().all())
                # Add the guild to the session and commit
                session.add(guild)
                await session.commit()

                return f"Guild {guild_id} added successfully."
            except Exception as error:
                print(error)