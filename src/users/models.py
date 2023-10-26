from datetime import datetime
from typing import List

from pydantic import EmailStr
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from core.models import Base
# from src.users.utils.password_hash import Password


class User(Base):
    username: Mapped[str] = mapped_column(
        String(length=50), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(length=30), nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(length=30), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String, unique=True, nullable=True, index=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    permissions: Mapped[List["UserPermission"]] = relationship("UserPermission", lazy="selectin")

    # @validates("password")
    # def _validate_password(self, key, password):
    #     password_field = getattr(type(self), key)
    #     return password_field.type.validator(password)


class Permission(Base):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    codename: Mapped[str] = mapped_column(String, unique=True, nullable=False)


class UserPermission(Base):
    codename: Mapped[String] = mapped_column(String, ForeignKey("users_permission.codename"))
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users_user.id"))

    __table_args__ = (UniqueConstraint("codename", "user_id"),)
