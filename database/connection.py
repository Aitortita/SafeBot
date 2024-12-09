from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base, Guild, WhitelistedDomain
from database import baseWhitelistedDomains, domainList
from sqlalchemy import select
from logging import getLogger
logger = getLogger("sqlalchemy.engine")

# variables for database connection
DBUSER = settings.DBUSER
DBPASSWORD = settings.DBPASSWORD
DBHOST = settings.DBHOST
DBNAME = settings.DBNAME

# SQLAlchemy database URL for MySQL connection.
db_url = f"postgresql+asyncpg://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBNAME}"

# Create the SQLAlchemy engine
engine = create_async_engine(db_url, pool_recycle=3600)

# Create a sessionmaker that produces async sessions
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

# Run an asynchronous function to create tables in the database
async def initializeDatabase():
    async with engine.begin() as conn:
        try:
            # This drops the tables from the database
            # await conn.run_sync(Base.metadata.drop_all) 
            # Creates the tables defined in your models
            await conn.run_sync(Base.metadata.create_all)
            logger.info(f"All DB models have been created")
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
async def initializeGuilds(discord_guilds: list[discord.Guild]) -> None:
    """ 
    Fetches all guilds and creates a row for each one
    """
    async with async_session() as session:
        async with session.begin():
            try:
                # Get all AbsoluteWhitelistedDomains from the WhitelistedDomain table
                base_whitelisted_domains = (await session.execute(select(WhitelistedDomain).where(WhitelistedDomain.domain_name.in_(domainList)))).scalars().all()

                # Get all stored guilds
                stored_guilds = (await session.execute(select(Guild).where(Guild.guild_id.in_(discord_guilds)))).scalars().all()

                # Filter unstored guilds
                stored_guilds_ids = [guild.guild_id for guild in stored_guilds]
                unstored_guilds = [guild_id for guild_id in discord_guilds if guild_id not in stored_guilds_ids]

                # Create new guild
                guilds = [Guild(id=str(uuid.uuid4()),guild_id=guild_id) for guild_id in unstored_guilds]

                # Associate whitelisted domains with each guild
                for guild in guilds:
                    guild.whitelisted_domains.extend(base_whitelisted_domains)
                
                session.add_all(guilds)
                await session.commit()
            except Exception as error:
                await session.rollback()
                logger.error(error)
            finally:
                await session.close()