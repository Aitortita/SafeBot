from typing import List, TYPE_CHECKING
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models import Base
import uuid

if TYPE_CHECKING:
    from . import ScannedLink

class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(36), default=str(uuid.uuid4()), unique=True, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    scanned_links: Mapped[List["ScannedLink"]] = relationship(back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, user_id={self.user_id})>"