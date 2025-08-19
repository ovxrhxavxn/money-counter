from ..config import BaseConfig


class SQLConfig(BaseConfig):
    db_host: str


config = SQLConfig()