from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "test_pool_object_from_user_handler"
logger = setup_logger(service_name)


async def test_pool_object_from_user_handler():
    # Here we get the pool connection
    pool = container.get_pool()
    if pool:
        try:
            logger.info(f"{Colors.CYAN}Performing database operations...{Colors.END}")

            # Acquire a connection from the pool
            async with pool.acquire() as connection:
                logger.info(f'Acquired a connection from the pool')
                # Acquire a cursor from the connection
                async with connection.cursor() as cursor:
                    # Perform any database operations here
                    logger.info(f'Acquired a cursor and attempting query')

                    await cursor.execute("SELECT version();")
                    result = await cursor.fetchone()
                    logger.info(f"{Colors.GREEN}Database version:{Colors.END} {result}")

        except Exception as e:
            logger.error(f"{Colors.RED}Error during database operations: {e}.{Colors.END}")

        finally:
            # Return the cursor and connection to the pool
            await return_cursor_connection_to_pool(cursor)
            logger.info(f"Successfully returned the cursor and connection to the pool!")
