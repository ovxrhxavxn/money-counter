from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ...fsms import UseModelStates
from ...services import CVModelsService


router = Router(name="Use YOLO8S")


@router.message(Command('use_yolo8s'))
async def use_yolo8s(message: Message, state: FSMContext):
    await state.set_state(UseModelStates.use_yolo8s)
    await message.answer('Отправьте изображение: ')


@router.message(UseModelStates.use_yolo8s)
async def process_image(message: Message, cv_models_service: CVModelsService, state: FSMContext):
    # 1. Give the user some feedback so they know the bot is working.
    await message.answer("Got your photo! Processing it now, please wait...")

    # 2. Get the highest resolution photo object from the list.
    photo = message.photo[-1]

    # 3. Download the file content into an in-memory buffer.
    #    message.bot gives you access to the bot instance that received the update.
    photo_buffer = await message.bot.download(photo.file_id)
    if not photo_buffer:
        # This can happen if the file is too old or something went wrong on TG's side
        await message.answer('Невозможно загрузить изображение. Попробуйте снова.')
        return

    # 4. Read the bytes from the buffer. This is what you'll send to your API.
    photo_bytes = photo_buffer.read()

    # 5. Get an instance of your service to call the backend.

    try:
        await cv_models_service.use_yolo8s(image=photo_bytes, chat_id=message.chat.id)
        await message.answer("Your image has been sent for processing! I'll send you the result when it's ready.")

    except Exception as e:
        await message.answer(str(e))
    finally:
        # 7. IMPORTANT: Clear the state so the user can send commands again.
        await state.clear()