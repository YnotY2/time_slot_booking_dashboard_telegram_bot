from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "fetch_time_slot_row_by_id"
logger = setup_logger(service_name)


async def fetch_time_slot_row_by_id(slot_id: int):
    """Fetch the time slot row by its given ID if it is not booked."""

    pool = container.get_pool()
    if pool:
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Query to fetch a specific time slot by ID
                    query_fetch_slot = """
                        SELECT start_time, end_time 
                        FROM time_slots 
                        WHERE id = %s
                          AND is_booked = FALSE
                    """
                    await cursor.execute(query_fetch_slot, (slot_id,))
                    result = await cursor.fetchone()

                    if not result:
                        logger.info(f"No available time slot found with ID {slot_id} or the slot is booked.")
                        return None  # No slot found or slot is booked

                    # Process the result
                    start_time, end_time = result
                    logger.info(f"Successfully fetched time slot with ID {slot_id}.")

                    # Return timeslot dat
                    time_slot_data = {
                        'start_time': start_time,
                        'end_time': end_time
                    }

        except Exception as e:
            logger.error(f"Error during database operations: {e}", exc_info=True)
            return None  # Error occurred

        finally:
            # The cursor is returned by the context manager, no need to explicitly return it to the pool
            await return_cursor_connection_to_pool(cursor)
            logger.info("Successfully returned the cursor and connection to the pool!")
            return time_slot_data
    else:
        logger.error("Database connection pool is not available.")
        return None