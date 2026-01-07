"""
Centralized app settings.

- Loads values from backend/.env (local) using pydantic-settings.
- Exposes DATABASE_URL used by SQLAlchemy and Alembic (later we’ll load Alembic from env too).
- Keep secrets out of Git: commit .env.example, but DO NOT commit .env.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Reads environment variables from a .env file in the backend folder
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    # Postgres connection settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "diabetes_db"
    DB_USER: str = "diabetes_user"
    DB_PASSWORD: str = "diabetes_password"

    @property
    def DATABASE_URL(self) -> str:
        """
        SQLAlchemy database URL.

        psycopg2 is our driver. Example:
        postgresql+psycopg2://user:password@host:port/dbname
        """
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
"""Singleton settings instance to be imported throughout the app."""
