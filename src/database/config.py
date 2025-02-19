from config import BaseConfig


class DBConfig(BaseConfig):

    db_url: str


config = DBConfig()