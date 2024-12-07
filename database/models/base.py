from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, primary_key=True, nullable=False)