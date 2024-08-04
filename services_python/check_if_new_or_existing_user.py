"""This code will check the telegram_ID of a client user
within db, then either returns True if they exist or False"""

from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "check_if_new_or_existing_user"
logger = setup_logger(service_name)


async def check_if_new_or_existing_user(user_id: str):
    """Ensure user_id matches table rules, is a string"""

    # Initialize the status variable containing bool lvalue
    status = False

    pool = container.get_pool()
    if pool:
        try:
            logger.info(f"{Colors.CYAN}Performing database operations...{Colors.END}")

            # Acquire a connection from the pool
            async with pool.acquire() as connection:
                logger.info(f'Acquired a connection from the pool')

                # Acquire a cursor from the connection
                async with connection.cursor() as cursor:
                    logger.info(f'Acquired a cursor and attempting query')

                    # Check if the user ID exists
                    query_exists = """
                        SELECT EXISTS(
                            SELECT 1 
                            FROM client_data 
                            WHERE telegram_id = %s
                        )
                    """
                    await cursor.execute(query_exists, (user_id,))
                    result = await cursor.fetchone()

                    if result is None:
                        logger.error(f"{Colors.RED}No result fetched from the query.{Colors.END}")
                        return False
                    user_exists = result[0]  # result is a tuple (exists,)

                    if user_exists:
                        logger.info(f"{Colors.GREEN}User ID {user_id} exists in the database.{Colors.END}")
                        status = True

                    else:
                        # Insert the user ID if it does not exist
                        query_insert = """
                            INSERT INTO client_data (telegram_id) 
                            VALUES (%s)
                        """
                        await cursor.execute(query_insert, (user_id,))
                        logger.info(f"{Colors.GREEN}User ID {user_id} added to the database.{Colors.END}")
                        status = True

        except Exception as e:
            logger.error(f"{Colors.RED}Error during database operations: {e}.{Colors.END}")
            status = False

        finally:
            # Return the cursor and connection to the pool
            await return_cursor_connection_to_pool(cursor)
            logger.info(f"Successfully returned the cursor and connection to the pool!")
            return status
    else:
        logger.error(f"{Colors.RED}Database connection pool is not available.{Colors.END}")
        return status
