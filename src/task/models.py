from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from src.users.models import User


class Task(Base):
    title: Mapped[str] = mapped_column(String(length=50), index=True)
    description: Mapped[str] = mapped_column(index=True)
    completed: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users_user.id'))
    owner: Mapped[User] = relationship(User, back_populates="tasks")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
