import os
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from submerged.gpt import logger

TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID: Optional[str] = os.getenv(
    "TELEGRAM_CHANNEL_ID"
)  # Can be chat ID or channel username like '@mychannel'
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")


async def post_to_telegram(image_bytes: bytes, description: str) -> bool:
    """
    Posts the image and its description to the configured Telegram channel.

    Args:
        image_bytes: The raw bytes of the image file.
        description: The text description to accompany the image.

    Returns:
        True if the message was sent successfully, False otherwise.
    """
    try:
        logger.info(
            f"Sending photo and description to Telegram channel: {TELEGRAM_CHANNEL_ID}"
        )
        # Send photo with caption
        await bot.send_photo(
            chat_id=TELEGRAM_CHANNEL_ID,
            photo=image_bytes,  # aiogram can handle raw bytes directly
            caption=description,
            # You can add more formatting or options here if needed
        )
        logger.info("Successfully posted to Telegram.")
        return True
    except TelegramAPIError as e:
        logger.error(f"Error sending message to Telegram: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during Telegram posting: {e}", exc_info=True
        )
        return False
