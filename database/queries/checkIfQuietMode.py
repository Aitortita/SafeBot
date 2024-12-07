from database.models import Guild
from database import async_session
from sqlalchemy import select
from logging import getLogger
logger = getLogger('sqlalchemy.engine')

async def check_if_quiet_mode(guild_id: int) -> bool:
    """
    Checks if the discord server has configured the quiet mode to not show any reactions

    Args:
        guild_id: int

    Returns:
        bool
    """
    async with async_session() as session:
        async with session.begin():
            try:
                guild = await session.execute(
                    select(Guild)
                    .where(Guild.guild_id == guild_id)
                )
                quiet = guild.scalar().quiet
                return quiet
            except Exception as error:
                await session.rollback()
                logger.error(error)
            finally:
                await session.close()