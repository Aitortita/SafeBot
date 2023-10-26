from sqlalchemy import String, Enum, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from . import Base

if TYPE_CHECKING:
    from . import User

class ScanResultEnum(PyEnum):
    SAFE = "safe"
    UNSAFE = "unsafe"

class ScannedLink(Base):
    __tablename__ = 'scanned_links'

    id: Mapped[str]= mapped_column(String(36), default=str(uuid.uuid4()), unique=True, primary_key=True, nullable=False)
    url: Mapped[str]= mapped_column(String, nullable=False)
    scan_result: Mapped[PyEnum]= mapped_column(Enum(ScanResultEnum), nullable=False)
    timestamp: Mapped[datetime]= mapped_column(server_default=func.now(), nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="scanned_links")

    def __repr__(self):
        return f"<ScannedLink(id={self.id}, url={self.url})>"