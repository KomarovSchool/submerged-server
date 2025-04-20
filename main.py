import logging

import uvicorn
from dotenv import load_dotenv

from submerged.gpt import logger, OPENAI_API_KEY
from submerged.telegram import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID


load_dotenv()

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

if not OPENAI_API_KEY:
    logger.error("FATAL: OPENAI_API_KEY environment variable not set.")
    exit("Set OPENAI_API_KEY environment variable.")
if not TELEGRAM_BOT_TOKEN:
    logger.error("FATAL: TELEGRAM_BOT_TOKEN environment variable not set.")
    exit("Set TELEGRAM_BOT_TOKEN environment variable.")
if not TELEGRAM_CHANNEL_ID:
    logger.error("FATAL: TELEGRAM_CHANNEL_ID environment variable not set.")
    exit("Set TELEGRAM_CHANNEL_ID environment variable.")

if __name__ == "__main__":
    uvicorn.run("submerged.web:app", host="0.0.0.0", port=8000, reload=True)
