from pydantic import BaseModel
from enum import StrEnum
from fastapi import File, UploadFile

class CVModel(StrEnum):

    YOLO8S = 'yolo8s',
    YOLO8N = 'yolo8n',
    YOLO8M = 'yolo8m'

class RequestToModel(BaseModel):

    user_name: str
    image: str


class TaskSchema(BaseModel):

    msg_id: str | None
    result_path: str | None

class TaskId(TaskSchema): 

    id: int | None
