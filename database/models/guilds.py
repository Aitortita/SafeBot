from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.models import Base
import uuid

class Guild(Base):
    __tablename__ = 'guilds'

    id = Column(String(36), default=str(uuid.uuid4()), unique=True, primary_key=True, nullable=False)
    guild_id = Column(Integer, unique=True, nullable=False)

    # Define the many-to-many relationship to safe_domains
    safe_domains = relationship('SafeDomain', secondary='guilds_safe_domains')
