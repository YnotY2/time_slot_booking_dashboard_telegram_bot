"""This function can place a specified time_slot ID either True or False
Making the entry to service either available for a user, or unavailable"""

"""return a 5 int PIN when 'is_booked' is set to TRUE.
if a time-slot 'is_booked' is set to FALSE, we remove the PIN."""

import random
import string

from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "manage_booking_time_slots"
logger = setup_logger(service_name)

async def manage_booking_time_slots(time_slot_id: int, book_time_slot: bool):
    """
    Updates the 'is_booked' status of a time slot in the database.

    Args:
        time_slot_id (int): The ID of the time slot to update.
        book_time_slot (bool): True to book the time slot, False to unbook it.

    Returns:
        bool: Status of the update operation (True if successful, False otherwise).
        str: A 5-digit PIN if booked, else an empty string.
    """
    pool = container.get_pool()

    if not pool:
        logger.error("Database connection pool is not available.")
        return None, ""

    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                if book_time_slot:
                    # Generate a 5-digit PIN
                    access_pin = ''.join(random.choices(string.digits, k=5))
                    update_query = """
                        UPDATE time_slots
                        SET is_booked = TRUE, access_pin = %s
                        WHERE id = %s
                    """
                    await cursor.execute(update_query, (access_pin, time_slot_id))
                    logger.info(f"Successfully booked time slot {time_slot_id}. Generated PIN: {access_pin}.")
                    return True, access_pin

                else:
                    # Explicitly remove the PIN when unbooking
                    update_query = """
                        UPDATE time_slots
                        SET is_booked = FALSE, access_pin = ''
                        WHERE id = %s AND is_booked = TRUE
                    """
                    await cursor.execute(update_query, (time_slot_id,))

                    if cursor.rowcount == 0:
                        # Check if the time slot was already unbooked or was not found
                        check_query = """
                            SELECT access_pin
                            FROM time_slots
                            WHERE id = %s
                        """
                        await cursor.execute(check_query, (time_slot_id,))
                        result = await cursor.fetchone()

                        if result is None:
                            logger.warning(f"Time slot {time_slot_id} was not found.")
                            return False, ""

                        else:
                            logger.warning(f"Time slot {time_slot_id} was not booked or already unbooked.")
                            return False, ""

                    logger.info(f"Successfully unbooked time slot {time_slot_id}.")
                    return True, ""

    except Exception as e:
        logger.error(f"Error during database operations: {e}")
        return None, ""

    finally:
        await return_cursor_connection_to_pool(cursor)
        logger.info("Operation completed.")