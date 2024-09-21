import dramatiq

from cv_models.cv_processing.yolo8model import YOLO8Model


@dramatiq.actor
def use_cv_model(cv_model: YOLO8Model, image: bytes):

    sum, procesed_image, _ = cv_model.use(image)

    return sum, procesed_image