from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    session: int = 1
