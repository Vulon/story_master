from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    host: str = "localhost"
    port: int = 7687


class Settings(BaseSettings):
    db_settings: DatabaseSettings = DatabaseSettings()
    session: int = 1
