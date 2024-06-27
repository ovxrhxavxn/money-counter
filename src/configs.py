from pydantic import Field
from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):

    host: str = Field(default=None, alias='DB_HOST')
    port: str | int = Field(default=None, alias='DB_PORT')
    name: str = Field(default=None, alias='DB_NAME')
    user: str = Field(default=None, alias='DB_USER')
    password: str = Field(default=None, alias='DB_PASSWORD')