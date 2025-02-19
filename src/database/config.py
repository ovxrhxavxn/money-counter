from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):

    db_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Игнорировать лишние переменные в .env
    )


config = DBConfig()