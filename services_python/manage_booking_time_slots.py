"""This function can place a specified time_slot ID either True or False
Making the entry to service either available for a user, or unavailable"""

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
    """
    pool = container.get_pool()

    if not pool:
        logger.error("Database connection pool is not available.")
        return False

    try:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                # Update the 'is_booked' status of the specified time slot
                update_query = """
                    UPDATE time_slots
                    SET is_booked = %s
                    WHERE id = %s
                """
                await cursor.execute(update_query, (book_time_slot, time_slot_id))
                logger.info(f"Successfully updated time slot {time_slot_id} to {'booked' if book_time_slot else 'available'}.")

    except Exception as e:
        logger.error(f"Error during database operations: {e}")
        return False

    finally:
        # If you are using an async connection pool, you don't need to manually return the cursor.
        # await return_cursor_connection_to_pool(cursor) # Commented out as it might not be necessary
        logger.info("Operation completed.")
        return True
