from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models import Base
import uuid

if TYPE_CHECKING:
    from . import Guild

class SafeDomain(Base):
    __tablename__ = 'safe_domains'

    id: Mapped[str] = mapped_column(String(36), default=str(uuid.uuid4()), primary_key=True)
    domain_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # Define the many-to-many relationship to guilds
    guilds: Mapped[List["Guild"]] = relationship(
        secondary="guilds_safe_domains",
        back_populates="safe_domains",
        )
    
    def __repr__(self):
        return f"<SafeDomain(id={self.id}, domain_name='{self.domain_name}')>"
