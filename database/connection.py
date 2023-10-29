from logging import getLogger
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base, Guild, WhitelistedDomain
from database import baseWhitelistedDomains, domainList
from sqlalchemy import select
logger = getLogger("sqlalchemy.engine")

# variables for database connection
DBUSER = settings.DBUSER
DBPASSWORD = settings.DBPASSWORD
DBHOST = settings.DBHOST
DBNAME = settings.DBNAME

# SQLAlchemy database URL for MySQL connection.
db_url = f"postgresql+asyncpg://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBNAME}"

# Create the SQLAlchemy engine
engine = create_async_engine(db_url, echo=True)

# Create a sessionmaker that produces async sessions
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

# Run an asynchronous function to create tables in the database
async def initializeDatabase():
    async with engine.begin() as conn:
        try:
            # await conn.run_sync(Base.metadata.drop_all) # This drops the tables from the database
            await conn.run_sync(Base.metadata.create_all) # This creates the tables defined in your models
            logger.info(f"DB: all models have been created")
            await conn.commit()
        except Exception as error:
            await conn.rollback()
            print(error)
        finally:
            await conn.close()

    async with async_session() as session:
        async with session.begin():
            try:
                # Bulk creates a base list of safe domains
                session.add_all(baseWhitelistedDomains)
                await session.commit()
            except Exception as error:
                await session.rollback()
                print(error)
            finally:
                await session.close()

import discord
import uuid
async def initializeGuilds(fetched_guilds: list[discord.Guild]) -> None:
    """ fetches all guilds and creates a database row for each one
    """
    async with async_session() as session:
        async with session.begin():
            try:
                # Get all AbsoluteWhitelistedDomains from the WhitelistedDomain table
                base_whitelisted_domains = await session.execute(select(WhitelistedDomain).where(WhitelistedDomain.domain_name.in_(domainList)))
                print("post base_whitelist query")

                # Create new guild
                guilds = [Guild(id=str(uuid.uuid4()),guild_id=guild.id) for guild in fetched_guilds]
                print(f"post guild creation: {guilds}")

                # Associate whitelisted domains with each guild
                for guild in guilds:
                    guild.whitelisted_domains.extend(base_whitelisted_domains.scalars().all())
                print(f"post guild extension")

                # Add the guild to the session and commit
                session.add_all(guilds)
                await session.commit()
                print("post commit")
            except Exception as error:
                print(error)
            finally:
                await session.close()