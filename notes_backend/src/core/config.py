from pydantic import BaseModel
from typing import List


class AppSettings(BaseModel):
    """Application runtime settings."""

    app_name: str = "Personal Notes API - Ocean Professional"
    # Allow all origins by default for ease of preview; lock down in production as needed.
    cors_allow_origins: List[str] = ["*"]
    database_url: str = "sqlite+aiosqlite:///./notes.db"


_settings = AppSettings()


# PUBLIC_INTERFACE
def get_app_settings() -> AppSettings:
    """Return application settings.

    This is a simple accessor for settings, enabling future extension to load from env.
    """
    return _settings
