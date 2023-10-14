from logging import getLogger
import asyncio
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database.models import Base
logger = getLogger("bot")

# variables for database connection
DBUSER = settings.DBUSER
DBPASSWORD = settings.DBPASSWORD
DBHOST = settings.DBHOST
DBNAME = settings.DBNAME

# SQLAlchemy database URL for MySQL connection.
db_url = f"postgresql+asyncpg://{DBUSER}:{DBPASSWORD}@{DBHOST}/{DBNAME}"

# Create the SQLAlchemy engine
engine = create_async_engine(db_url, echo=True, future=True)

# Create a sessionmaker that produces async sessions
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Run an asynchronous function to create tables in the database
async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all) # This creates the tables defined in your models
            logger.info(f"DB: all models have been created")
    except Exception as error:
        print(error)
asyncio.run(create_tables())