from ..config import BaseConfig


class CVModelGRPCConfig(BaseConfig):
    grpc_host: str


config = CVModelGRPCConfig()