import datetime
import uuid

from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }

    @declared_attr
    def __tablename__(self):
        return self.__module__.split('.')[1] + '_' + self.__name__.lower()
