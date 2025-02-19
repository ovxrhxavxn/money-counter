import dramatiq

from cv_models.core.yolo8model import YOLO8Model


@dramatiq.actor
@dramatiq.asyncio.async_to_sync
async def use_cv_model(cv_model: YOLO8Model, image: bytes):

    sum, procesed_image, _ = cv_model.use(image)

    return sum, procesed_image