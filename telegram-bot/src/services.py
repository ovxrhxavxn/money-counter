from .repositories import AbstractFastAPIServiceRepository


class CVModelsService:
    def __init__(self, repo: type[AbstractFastAPIServiceRepository]):
        self._repo = repo()


    async def use_yolo8s(self, image: bytes, chat_id: int):
        return await self._repo.use_yolo8s(image, chat_id)
    
    async def use_yolo8n(self, image: bytes, chat_id: int):
        return await self._repo.use_yolo8n(image, chat_id)
    
    async def use_yolo8m(self, image: bytes, chat_id: int):
        return await self._repo.use_yolo8m(image, chat_id)