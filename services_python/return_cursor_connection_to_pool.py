import asyncio
from utils.colors import Colors
from utils.logger import setup_logger

# Set up logger with service name
service_name = "return_cursor_connection_to_pool"
logger = setup_logger(service_name)

async def return_cursor_connection_to_pool(cursor):
    logger.info(f"{Colors.CYAN}Attempting to return connection and the cursor to pool for database:{Colors.END}")

    try:
        cursor.close()  # No need to await cursor.close() as it's a sync method in aiopg
        logger.info(f"{Colors.GREEN}Successfully closed cursor.{Colors.END}")
    except Exception as e:
        logger.error(f"{Colors.RED}Error closing cursor: {e}.{Colors.END}")
        return False

    # Return connection to the pool automatically when exiting the context manager
    return True