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
                for domain in absolute_safe_domains:
                    print(f"absolute_safe_domains: {domain}")

                # Associate guild with all AbsoluteSafeDomains
                guild.safe_domains.extend(absolute_safe_domains)

                # Add the guild to the session and commit
                session.add(guild)
                await session.commit()

                return "Guild added successfully."
            except Exception as error:
                print(error)