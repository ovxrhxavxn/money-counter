from typing import Protocol

import aiohttp

from .configs import fastapi_service_config


class AbstractFastAPIServiceRepository(Protocol):
    async def use_yolo8s(self, image: bytes, chat_id: int) -> None:
        ...

    async def use_yolo8n(self, image: bytes, chat_id: int) -> None:
        ...

    async def use_yolo8m(self, image: bytes, chat_id: int) -> None:
        ...


class FastAPIServiceRepository:
    async def _send_image_to_model(self, model_name: str, image: bytes, chat_id: int) -> None:
        """
        A private helper method to send an image to a specific model endpoint.
        This avoids code duplication.
        """
        # The URL for the specific model endpoint
        url = f'{fastapi_service_config.base_url}/cv/model/{model_name}'

        # 1. Create a FormData object
        data = aiohttp.FormData()

        # 2. Add the fields your FastAPI endpoint expects.
        #    The names MUST match the parameter names in your FastAPI function.
        #    - 'chat_id': This is the string parameter.
        #    - 'image': This is the UploadFile parameter.
        data.add_field('chat_id', str(chat_id))
        data.add_field(
            'image',
            image, # The raw bytes of the image
            filename='photo.jpg', # A generic filename is fine
            content_type='image/jpeg' # The content type
        )

        async with aiohttp.ClientSession() as session:
            try:
                # 3. Send the POST request with the `data` payload
                async with session.post(url, data=data) as response:
                    # 4. It's crucial to check the response!
                    response.raise_for_status() # This will raise an error for 4xx/5xx responses
            except aiohttp.ClientError:
                # You might want to re-raise the exception or handle it here
                raise

    async def use_yolo8s(self, image: bytes, chat_id: int) -> None:
        await self._send_image_to_model("yolo8s", image, chat_id)

    async def use_yolo8n(self, image: bytes, chat_id: int) -> None:
        await self._send_image_to_model("yolo8n", image, chat_id)

    async def use_yolo8m(self, image: bytes, chat_id: int) -> None:
        await self._send_image_to_model("yolo8m", image, chat_id)
