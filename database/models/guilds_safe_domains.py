from sqlalchemy import Table, Column, ForeignKey
from database.models import Base

GuildWhitelistedDomainAssociation = Table(
    'guilds_whitelisted_domains',
    Base.metadata,
    Column("guild_id", ForeignKey('guilds.id'), primary_key=True),
    Column("whitelisted_domain_id", ForeignKey('whitelisted_domains.id'), primary_key=True),
)