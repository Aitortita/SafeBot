from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.models import Base
import uuid

class SafeDomain(Base):
    __tablename__ = 'safe_domains'

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)
    domain_name = Column(String(255), unique=True, nullable=False)

    # Define the many-to-many relationship to guilds
    guilds = relationship('Guild', secondary='guilds_safe_domains')

    def __repr__(self):
        return f"<SafeDomain(id={self.id}, domain_name='{self.domain_name}')>"
