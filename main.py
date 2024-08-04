import asyncio
import time

from aiogram import Dispatcher
from bot.handlers.user_handlers import user_router
from dependencies import container      # This takes care of the connection pool to database, ensuring we can share pool.

from services_python.bot_instance import bot
from services_python.initialize_connection_pool import initialize_connection_pool

# Modify the function of adding user to database only after they have actually bought-voucher for free.

from utils.logger import setup_logger
logger = setup_logger(service_name="main")

def register_routers(dp: Dispatcher) -> None:
    """Registers routers"""
    dp.include_router(user_router)

async def main() -> None:
    """The main function which will execute our event loop and start polling. [listening for user events]"""
    # Initialize the connection pool only needed once.
    # I can pass the pool object to all my functions and it will work fine asynchronous.
    pool = await initialize_connection_pool()
    container.set_pool(pool)        # We pass the pool to the container? (its a class tho)
    dp = Dispatcher()

    register_routers(dp)
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Shutting down...")

    finally:
        logger.info("Closing the connection pool...")
        container.get_pool().close()
        await container.get_pool().wait_closed()
        logger.info("Connection pool closed. Exiting.")


if __name__ == "__main__":
    logger.info("Starting main.py process, telegram bot live!")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received SIGINT signal. Exiting...")



