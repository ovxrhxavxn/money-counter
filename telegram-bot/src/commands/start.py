from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    pass