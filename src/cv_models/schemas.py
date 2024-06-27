from pydantic import BaseModel, Field
from enum import StrEnum

class CVModel(StrEnum):

    YOLO8S = 'yolo8s',
    YOLO8N = 'yolo8n',
    YOLO8M = 'yolo8m'

class RequestToModel(BaseModel):

    user_name: str
    image: bytes