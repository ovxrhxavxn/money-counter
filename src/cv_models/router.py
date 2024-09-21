import base64
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from PIL.Image import Image

from .schemas import CVModelEnum, TaskSchema, CVModelSchema, TaskResult
from .services import CVModelsService, TasksService
from .dependencies import (

    get_cv_models_service, 
    get_tasks_service
)


router = APIRouter (

    prefix='/cv',
    tags=['CV Model']
)


@router.post(f'/models/{CVModelEnum.YOLO8S}', status_code=202)
async def use_yolo8s(

    user_name: str, 
    image: UploadFile, 
    service: Annotated[CVModelsService, Depends(get_cv_models_service)]):

    try:

        return await service.use_yolo8s(user_name, image)
    
    except IndexError:
        
        raise HTTPException(404, detail='The user doesn`t exist')
    

@router.post(f'/models/{CVModelEnum.YOLO8M}', status_code=202)
async def use_yolo8m(
    
    user_name: str, 
    image: UploadFile, 
    service: Annotated[CVModelsService, Depends(get_cv_models_service)]):

    try:

        return await service.use_yolo8s(user_name, image)

    except IndexError:
        
        raise HTTPException(404, detail='The user doesn`t exist')


@router.post(f'/models/{CVModelEnum.YOLO8N}', status_code=202)
async def use_yolo8n(
    
    user_name: str, 
    image: UploadFile, 
    service: Annotated[CVModelsService, Depends(get_cv_models_service)]):

    try:

        return await service.use_yolo8n(user_name, image)
    
    except IndexError:

        raise HTTPException(404, detail='The user doesn`t exist')


@router.get('/models/tasks/{task_id}', response_model=TaskResult)
async def get_task_result(
    
    task_id: str, 
    service: Annotated[TasksService, Depends(get_tasks_service)]
    
    ):

    try:

        task = await service.check_task_result(task_id)

        img_bytes = await (Path(task.image_id).resolve())

        encoded_string = base64.b64encode(img_bytes).decode()

        return JSONResponse(content={

            'image' : encoded_string,
            'total' : task.result_sum
        })
    
    except ValueError:

        raise HTTPException(202, detail="The task is in processing")


@router.get('/models/{model_name}', response_model=CVModelSchema)
async def get_model(
    
    model_name: str,
    service: Annotated[CVModelsService, Depends(get_cv_models_service)]
    
    ):

    try:

        return await service.get(model_name)
    
    except IndexError:

        raise HTTPException(404, detail='The model doesn`t exist')
    

@router.patch('/models/{model_name}/cost')
async def change_model_cost(
    
    model_name: str, 
    new_cost: int,
    service: Annotated[CVModelsService, Depends(get_cv_models_service)]
    
    ):

    await service.change_cost(model_name, new_cost)
    

# @router.get('/models/tasks/history/{user_name}')
# async def get_user_image_history(user_name: str, session: AsyncSession = Depends(SQLAlchemyHandler().get_async_session)):

#     base64_images = []

#     crud = SQLAlchemyCRUD(session)

#     paths = await crud.get_images_paths_by_user_id(await crud.get_user_id(user_name))

#     for path in paths:

#         base64_images.append(

#             base64.b64encode(Image().read(Path(path).resolve())).decode()
#         )

#     return JSONResponse(content=base64_images)