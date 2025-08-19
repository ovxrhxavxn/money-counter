from ..config import BaseConfig


class RQConfig(BaseConfig):
    redis_host: str
    redis_port: int


config = RQConfig()