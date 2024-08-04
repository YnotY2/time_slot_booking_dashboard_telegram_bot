from aiogram import Bot, types
from config.settings import telegram_bot_token

from utils.logger import setup_logger
logger = setup_logger(service_name="bot_instance")


bot = Bot(
    token=telegram_bot_token
)

