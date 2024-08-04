# Revised main function

import asyncio
from services_python.initialize_connection_pool import initialize_connection_pool
from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool

from utils.colors import Colors
from utils.logger import setup_logger

# Set up logger with service name
service_name = "test_database_main"
logger = setup_logger(service_name)

async def main():
    # Initialize the connection pool only needed once.
    # I can pass the pool object to all my functions and it will work fine asynchronous.
    pool = await initialize_connection_pool()

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

                    # Return the cursor and connection to the pool
                    await return_cursor_connection_to_pool(cursor, connection, pool)
                    logger.info(f"Successfully returned the cursor and connection to the pool!")

        except Exception as e:
            logger.error(f"{Colors.RED}Error during database operations: {e}.{Colors.END}")

        finally:
            try:
                # Ensure the pool is closed when the application is shutting down
                pool.close()
                await pool.wait_closed()

            except Exception as e:
                logger.error(f"Error while closing database connection pool: {e}")

if __name__ == "__main__":
    asyncio.run(main())
