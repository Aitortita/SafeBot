from sqlalchemy import Table, Column, ForeignKey
from database.models import Base

GuildSafeDomainAssociation = Table(
    'guilds_safe_domains',
    Base.metadata,
    Column("guild_id", ForeignKey('guilds.id'), primary_key=True),
    Column("safe_domain_id", ForeignKey('safe_domains.id'), primary_key=True),
)