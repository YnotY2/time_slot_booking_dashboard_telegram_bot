
from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "fetch_user_entered_access_pin_stored_db"
logger = setup_logger(service_name)
async def fetch_user_entered_access_pin_stored_db(user_id: str):
    """Retrieve the PIN for a user from the database, or insert a new row if the user does not exist."""
    logger.info(f"Within 'get_pin' function, user_id: {user_id}")
    pool = container.get_pool()
    if pool:
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # First, attempt to fetch the PIN for the user
                    query_fetch_pin = """
                        SELECT pin FROM pins WHERE user_id = %s
                    """
                    await cursor.execute(query_fetch_pin, (user_id,))
                    row = await cursor.fetchone()

                    if row:
                        # If the PIN exists, return it
                        pin = row[0]
                        logger.info(f"Retrieved PIN for user {user_id}.")
                        logger.info(f"Retrieved PIN 'get_pin' {[pin]}.")
                        return pin
                    else:
                        # If the PIN does not exist, insert a new row with the user_id and fresh first PIN
                        query_insert_user = """
                            INSERT INTO pins (user_id, pin)
                            VALUES (%s, %s)
                        """
                        await cursor.execute(query_insert_user, (user_id, ""))
                        logger.info(f"Inserted new row for user {user_id} with empty PIN.")
                        return None

        except Exception as e:
            logger.error(f"Error fetching or inserting PIN: {e}")
            return None
        finally:
            await return_cursor_connection_to_pool(cursor)