from aiogram import Router

from .use_yolo8s import router as use_yolo8s_router
from .use_yolo8n import router as use_yolo8n_router
from .use_yolo8m import router as use_yolo8m_router


router = Router()

subrouters = [use_yolo8s_router, use_yolo8n_router, use_yolo8m_router]

router.include_routers(*subrouters)