from pydantic import BaseModel
from enum import StrEnum
from fastapi import File, UploadFile

class CVModelEnum(StrEnum):

    YOLO8S = 'yolo8s',
    YOLO8M = 'yolo8m',
    YOLO8N = 'yolo8n'

class CVModelSchema(BaseModel):

    name: str
    cost: int

class RequestToModel(BaseModel):

    user_name: str
    image: str


class TaskSchema(BaseModel):

    cv_model_id: int
    msg_id: str | None
    result_path: str | None

class TaskId(TaskSchema): 

    id: int | None


class ImageHistorySchema(BaseModel):

    user_id: int
    task_id: int

