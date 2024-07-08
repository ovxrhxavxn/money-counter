from pydantic import BaseModel
from sqlalchemy.types import Date
from enum import StrEnum


class CVModelEnum(StrEnum):

    YOLO8N = 'yolo8n',
    YOLO8S = 'yolo8s',
    YOLO8M = 'yolo8m'

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
    result_sum: float | None

class TaskId(TaskSchema): 

    id: int | None


class ImageHistorySchema(BaseModel):

    user_id: int
    task_id: int


class TaskResult(BaseModel):

    image: str
    total: float