from typing import List, TYPE_CHECKING
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models import Base
import uuid

if TYPE_CHECKING:
    from . import SafeDomain

class Guild(Base):
    __tablename__ = 'guilds'

    id: Mapped[str] = mapped_column(String(36), default=str(uuid.uuid4()), unique=True, primary_key=True, nullable=False)
    guild_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    # Define the many-to-many relationship to safe_domains
    safe_domains: Mapped[List["SafeDomain"]] = relationship(
        secondary="guilds_safe_domains",
        back_populates="guilds"
        )
    
    def __repr__(self):
        return f"<Guild(id={self.id}, guild_id='{self.guild_id}')>"