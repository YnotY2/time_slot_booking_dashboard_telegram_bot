
from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "delete_user_entered_access_pin_db"
logger = setup_logger(service_name)
async def delete_user_entered_access_pin_db(user_id: str):
    """Clear the PIN entry for a user."""
    pool = container.get_pool()
    if pool:
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    query_clear_pin = """
                        DELETE FROM pins WHERE user_id = %s
                    """
                    await cursor.execute(query_clear_pin, (user_id,))
                    logger.info(f"Cleared PIN for user {user_id}.")
        except Exception as e:
            logger.error(f"Error clearing PIN: {e}")
        finally:
            await return_cursor_connection_to_pool(cursor)