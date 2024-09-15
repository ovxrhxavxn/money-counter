import base64
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from PIL.Image import Image


from .schemas import CVModelEnum, TaskSchema, CVModelSchema, TaskResult
from tasks import TasksSet
from database.database import SQLAlchemyDBHelper
from database.crud import SQLAlchemyCRUD


router = APIRouter (

    prefix='/cv',
    tags=['CV Model']
)


@router.post(f'/models/{CVModelEnum.YOLO8S}', status_code=202)
async def use_yolo8s(user_name: str, image: UploadFile, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

    crud = SQLAlchemyCRUD(session)

    cv_model_id = await crud.get_cv_model_id(CVModelEnum.YOLO8S)

    await crud.add_task(TaskSchema(cv_model_id=cv_model_id,result_path=None, msg_id=None, result_sum=None))

    last_task = await crud.get_last_task()

    try:

        await crud.get_user(user_name)

        path = Path(f'database\\images\\{last_task.id}.jpeg').resolve()

        Image().save(path, image.file.read())

        msg = TasksSet.use_yolo8s.send(user_name, last_task.id, str(path))

        await crud.update_task_msg_id(last_task.id, msg.message_id)

    except IndexError:

        await crud.delete_task(last_task.id)

        raise HTTPException(404, detail='The user doesn`t exist')
    
    except Exception:

        await crud.delete_task(last_task.id)
    
    else:

        return {'task_id' : msg.message_id}
    

@router.post(f'/models/{CVModelEnum.YOLO8M}', status_code=202)
async def use_yolo8m(user_name: str, image: UploadFile, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

    crud = SQLAlchemyCRUD(session)

    cv_model_id = await crud.get_cv_model_id(CVModelEnum.YOLO8M)

    await crud.add_task(TaskSchema(cv_model_id=cv_model_id,result_path=None, msg_id=None, result_sum=None))

    last_task = await crud.get_last_task()

    try:

        await crud.get_user(user_name)

        path = Path(f'database\\images\\{last_task.id}.jpg').resolve()

        Image().save(path, image.file.read())

        msg = TasksSet.use_yolo8m.send(user_name, last_task.id, str(path))

        await crud.update_task_msg_id(last_task.id, msg.message_id)

    except IndexError:

        await crud.delete_task(last_task.id)

        raise HTTPException(404, detail='The user doesn`t exist')
    
    except Exception:

        await crud.delete_task(last_task.id)
    
    else:

        return {'task_id' : msg.message_id}


@router.post(f'/models/{CVModelEnum.YOLO8N}', status_code=202)
async def use_yolo8n(user_name: str, image: UploadFile, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

    crud = SQLAlchemyCRUD(session)

    cv_model_id = await crud.get_cv_model_id(CVModelEnum.YOLO8M)

    await crud.add_task(TaskSchema(cv_model_id=cv_model_id,result_path=None, msg_id=None, result_sum=None))

    last_task = await crud.get_last_task()

    try:

        await crud.get_user(user_name)

        path = Path(f'database\\images\\{last_task.id}.jpg').resolve()

        Image().save(path, image.file.read())

        msg = TasksSet.use_yolo8n.send(user_name, last_task.id, str(path))

        await crud.update_task_msg_id(last_task.id, msg.message_id)

    except IndexError:

        await crud.delete_task(last_task.id)

        raise HTTPException(404, detail='The user doesn`t exist')
    
    except Exception:

        await crud.delete_task(last_task.id)
    
    else:

        return {'task_id' : msg.message_id}

@router.get('/models/tasks/{task_id}', response_model=TaskResult)
async def get_task_result(task_id: str, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

    task = await SQLAlchemyCRUD(session).get_task_by_msg_id(task_id)

    if task.result_path is None:
    
        raise HTTPException(202, detail='The task is in processing')
    

    img_bytes = Image().read(Path(task.result_path).resolve())

    encoded_string = base64.b64encode(img_bytes).decode()
    

    return JSONResponse(content={

        'image' : encoded_string,
        'total' : task.result_sum
    })


@router.get('/models/{model_name}', response_model=CVModelSchema)
async def get_model(model_name: str, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

    try:

        return await SQLAlchemyCRUD(session).get_cv_model(model_name)
    
    except IndexError:

        raise HTTPException(404, detail='The model doesn`t exist')
    

@router.patch('/models/{model_name}/cost')
async def change_model_cost(model_name: str, new_cost: int, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

    await SQLAlchemyCRUD(session).change_cv_model_cost(model_name, new_cost)
    

@router.get('/models/tasks/history/{user_name}')
async def get_user_image_history(user_name: str, session: AsyncSession = Depends(SQLAlchemyDBHelper().get_async_session)):

    base64_images = []

    crud = SQLAlchemyCRUD(session)

    paths = await crud.get_images_paths_by_user_id(await crud.get_user_id(user_name))

    for path in paths:

        base64_images.append(

            base64.b64encode(Image().read(Path(path).resolve())).decode()
        )

    return JSONResponse(content=base64_images)