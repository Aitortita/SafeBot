from sqlalchemy import Column, Integer, ForeignKey, String
from database.models.base import Base


class GuildSafeDomainAssociation(Base):
    __tablename__ = 'guilds_safe_domains'

    guild_id = Column(String(36), ForeignKey('guilds.id'), primary_key=True)
    safe_domain_id = Column(String(36), ForeignKey('safe_domains.id'), primary_key=True)