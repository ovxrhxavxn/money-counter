import asyncio

from aiogram import Bot, Dispatcher

from .src.dependencies import get_cv_model_service
from .src.commands.start import router as start_router
from .src.commands.use_cv_models.use_cv_model import router as use_cv_models_router
from .src.configs import bot_config


dp = Dispatcher()
bot = Bot(token=bot_config.bot_token)
routers = [start_router, use_cv_models_router]

async def main():
    dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
            bot, 
            cv_models_service = get_cv_model_service()
        )
    

if __name__ == '__main__':
    asyncio.run(main())