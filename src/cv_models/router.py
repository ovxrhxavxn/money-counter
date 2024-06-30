from fastapi import APIRouter

from .schemas import RequestToModel, CVModel

class CVAPIRouterWrapper:

    __ROUTER = APIRouter(

        prefix='/cv',
        tags=['CV Model']
    )

    @property
    def router(self):
        return self.__ROUTER

    @staticmethod
    @__ROUTER.post(f'/{CVModel.YOLO8S}')
    async def use_yolo8s(request: RequestToModel):

        pass
    
    @staticmethod
    @__ROUTER.post(f'/{CVModel.YOLO8M}')
    async def use_yolo8m(request: RequestToModel):

        pass

    @staticmethod
    @__ROUTER.post(f'/{CVModel.YOLO8N}')
    async def use_yolo8n(request: RequestToModel):

        pass
