from database.models import Guild, SafeDomain
from database import async_session

async def add_guild(guild_id):
    async with async_session() as session:
        try:
            # Create new guild
            guild = Guild(id=guild_id)

            # Get all AbsoluteSafeDomains from the SafeDomain table
            absolute_safe_domains = await session.query(SafeDomain).filter_by(absolute=True).all()

            # Associate guild with all AbsoluteSafeDomains
            guild.safe_domains.extend(absolute_safe_domains)

            # Add the guild to the session and commit
            await session.add(guild)
            await session.commit()

            return True, "Guild and domain added successfully."

        except Exception as e:
            session.rollback()
            return False, f"Error: {e}"

        finally:
            session.close()
