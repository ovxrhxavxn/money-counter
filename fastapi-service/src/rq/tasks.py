
# fastapi-service/src/rq/tasks.py

import grpc
import asyncio
from aiogram import Bot
from aiogram.types import BufferedInputFile

# We need the generated protobuf files
from ..money_counter_protos.generated import cv_pb2, cv_pb2_grpc
# We also need the config to know where the gRPC server is
from ..cv_models.config import config as cv_config
# And now we need the bot token config
from ..config import telehgram_bot_config as bot_config


def process_image_with_yolo(model_type_enum_value: int, image_bytes: bytes, chat_id: int):
    """
    This function runs in the RQ worker.
    It creates its own gRPC channel, makes the call, gets the result,
    and then sends the result back to the user via Telegram.
    """
    result_image = None

    # The worker creates the channel, it is not passed from the web server.
    with grpc.insecure_channel(cv_config.grpc_host) as channel:
        stub = cv_pb2_grpc.ComputerVisionStub(channel)

        try:
            request = cv_pb2.ImageRequest(
                image_data=image_bytes,
                model_type=model_type_enum_value # Use the integer value passed to the queue
            )
            print(f"Worker processing image for chat_id {chat_id} with model {model_type_enum_value}")
            response = stub.ProcessImage(request, timeout=30)
            result_image = response.image_data

            asyncio.run(_send_result(result_image, chat_id))

        except grpc.RpcError as e:
            # Handle gRPC errors inside the worker
            print(f"gRPC call failed for chat_id {chat_id}: {e}")
            # Potentially notify the user of the failure
            # We'll do this outside the try/except block
        except Exception as e:
            print(f"An unexpected error occurred in the worker for chat_id {chat_id}: {e}")


# We need an async function to call the aiogram methods
async def _send_result(result_image, chat_id: int):
    bot = Bot(token=bot_config.bot_token)
    try:
        if result_image:
            # If we have an image, send it as a photo
            photo_to_send = BufferedInputFile(result_image, filename="result.jpg")
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo_to_send,
                caption="Here is your processed image!"
            )
            print(f"Successfully sent processed image to chat_id {chat_id}")
        else:
            # If result_image is None, it means an error occurred
            await bot.send_message(
                chat_id=chat_id,
                text="Sorry, something went wrong while processing your image. Please try again later."
            )
            print(f"Sent error message to chat_id {chat_id}")
    except Exception as e:
        # This catches errors with sending the message itself (e.g., bot blocked by user)
        print(f"Failed to send message to Telegram for chat_id {chat_id}: {e}")
    finally:
        # It's good practice to close the bot's session
        await bot.session.close()