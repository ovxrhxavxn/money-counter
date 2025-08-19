from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Form
from rq import Queue

from .enums import CVModel
from ..rq.tasks import process_image_with_yolo
from ..rq.dependencies import get_rq_queue
from ..money_counter_protos.generated import cv_pb2 


router = APIRouter(
    prefix="/cv/model",
    tags=["CV models"]
)


@router.post(f"/{CVModel.YOLO8S}")
async def use_yolo8s(
                    chat_id: Annotated[int, Form()],
                    image: UploadFile,
                    rq_queue: Annotated[Queue, Depends(get_rq_queue)]
    ):

    image_bytes = await image.read()
    rq_queue.enqueue(process_image_with_yolo, cv_pb2.YOLO8S, image_bytes, chat_id)


@router.post(f"/{CVModel.YOLO8N}")
async def use_yolo8n(
                    chat_id: Annotated[int, Form()],
                    image: UploadFile,
                    rq_queue: Annotated[Queue, Depends(get_rq_queue)]
    ):

    image_bytes = await image.read()
    rq_queue.enqueue(process_image_with_yolo, cv_pb2.YOLO8N, image_bytes, chat_id)


@router.post(f"/{CVModel.YOLO8M}")
async def use_yolo8m(
                    chat_id: Annotated[int, Form()],
                    image: UploadFile,
                    rq_queue: Annotated[Queue, Depends(get_rq_queue)]
    ):

    image_bytes = await image.read()
    rq_queue.enqueue(process_image_with_yolo, cv_pb2.YOLO8M, image_bytes, chat_id)