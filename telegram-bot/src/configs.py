from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Игнорировать лишние переменные в .env
    )


class BotConfig(BaseConfig):
    bot_token: str


bot_config = BotConfig()


class FastAPIServiceConfig(BaseConfig):
    fastapi_host: str
    fastapi_port: int

    @property
    def base_url(self) -> str:
        return f'{self.fastapi_host}:{self.fastapi_port}'


fastapi_service_config = FastAPIServiceConfig()