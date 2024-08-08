from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "insert_or_update_user_entered_access_pin_db"
logger = setup_logger(service_name)

async def insert_or_update_user_entered_access_pin_db(user_id: str, new_digit: str):
    """Insert or update the PIN for a user in the database.
    It appends the new digit if a PIN exists and has fewer than 5 digits.
    If the PIN is already 5 digits long, no update is made.
    If no PIN exists, it starts a new PIN.
    """
    pool = container.get_pool()
    if pool:
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Fetch the current PIN for the user
                    query_fetch_pin = """
                        SELECT pin FROM pins WHERE user_id = %s
                    """
                    await cursor.execute(query_fetch_pin, (user_id,))
                    row = await cursor.fetchone()

                    if row:
                        # If a PIN exists, append the new digit if the PIN is less than 5 digits pin is string  tho
                        current_pin = row[0]
                        if len(current_pin) <= 4:
                            updated_pin = current_pin + new_digit
                            if len(updated_pin) >= 5:
                                updated_pin = updated_pin[:5]  # Trim to first 5 digits if it exceeds

                            # Update the PIN in the database if we have received 5 pin codes pressed.
                            query_update_pin = """
                                UPDATE pins
                                SET pin = %s
                                WHERE user_id = %s
                            """

                            await cursor.execute(query_update_pin, (updated_pin, user_id))
                            logger.info(f"Current PIN: {current_pin}")
                            logger.info(f"Inserted or updated PIN for user {user_id}.")
                            logger.info(f"Updated PIN: {updated_pin}.")

                        else:
                            # If the PIN is already 5 digits, do nothing
                            logger.info(f"PIN already completed for user {user_id}.")
                    else:
                        # If no PIN exists, insert a new PIN
                        new_pin = new_digit
                        query_insert_pin = """
                            INSERT INTO pins (user_id, pin)
                            VALUES (%s, %s)
                        """
                        await cursor.execute(query_insert_pin, (user_id, new_pin))
                        logger.info(f"Inserted new first PIN-Digit for user {user_id}.")

        except Exception as e:
            logger.error(f"Error inserting or updating PIN: {e}")
        finally:
            await return_cursor_connection_to_pool(cursor)