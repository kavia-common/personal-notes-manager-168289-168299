from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.database import create_database, dispose_engine


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Manage startup and shutdown lifecycle tasks."""
    # Startup: prepare database
    await create_database()
    yield
    # Shutdown: dispose database connections
    await dispose_engine()
