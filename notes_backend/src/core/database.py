from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

from src.core.config import get_app_settings

Base = declarative_base()

_engine: AsyncEngine | None = None
# Session factory for creating AsyncSession instances
_SessionLocal: sessionmaker | None = None


# PUBLIC_INTERFACE
def get_engine() -> AsyncEngine:
    """Return a singleton async SQLAlchemy engine for the internal notes database."""
    global _engine
    if _engine is None:
        settings = get_app_settings()
        _engine = create_async_engine(settings.database_url, future=True, echo=False)
    return _engine


# PUBLIC_INTERFACE
def get_sessionmaker() -> sessionmaker:
    """Return a sessionmaker bound to the singleton engine."""
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _SessionLocal


# PUBLIC_INTERFACE
async def create_database() -> None:
    """Create database tables if not exist."""
    engine = get_engine()
    async with engine.begin() as conn:
        # SQLite pragmas for better integrity
        await conn.execute(text("PRAGMA foreign_keys=ON;"))
        await conn.run_sync(Base.metadata.create_all)


# PUBLIC_INTERFACE
async def dispose_engine() -> None:
    """Dispose the engine on application shutdown."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
