from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config.db import settings_db


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = create_async_engine(
            settings_db.database_url, future=True, echo=settings_db.DB_ECHO_LOG
        )
        self._session_local = async_scoped_session(
            async_sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False),
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        session: AsyncSession = self._session_local()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
