from pydantic import BaseModel

from .enums import CVModelEnum


class CVModelSchema(BaseModel):

    name: CVModelEnum
    cost: int


class TaskSchema(BaseModel):

    cv_model_id: int
    msg_id: str | None
    image_id: int | None
    result_sum: float | None


class TaskId(TaskSchema): 

    id: int | None


class TaskHistorySchema(BaseModel):

    user_id: int
    task_id: int


class TaskResult(BaseModel):

    image: str
    total: float