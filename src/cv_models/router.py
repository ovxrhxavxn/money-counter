from fastapi import APIRouter

from .schemas import RequestToModel, CVModel

router = APIRouter(

    prefix='/cv',
    tags=['CV Model']
)

@router.post(f'/{CVModel.YOLO8S}')
async def use_yolo8s(request: RequestToModel):

    pass

@router.post(f'/{CVModel.YOLO8M}')
async def use_yolo8m(request: RequestToModel):

    pass

@router.post(f'/{CVModel.YOLO8N}')
async def use_yolo8n(request: RequestToModel):

    pass
