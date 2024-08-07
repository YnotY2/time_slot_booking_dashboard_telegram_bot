"""Delete Old Time Slots:

    Remove time slots that have ended (i.e., their end_time is before the current time).

Insert New Time Slots:

    Insert new time slots for the next 46 hours if they do not already exist.
    Ensure that new time slots are inserted with is_booked = FALSE.

Avoid Updating Existing Time Slots:

    Existing time slots with is_booked = TRUE should not be modified or affected
    by this process."""

import asyncio

from datetime import datetime, timedelta
import pytz

from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "fetch_all_available_time_slots"
logger = setup_logger(service_name)
from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool


async def populate_time_slots():
    """Populate the database with time slots for the next 46 hours, refreshing as needed."""
    """I can ensure that while populating, booked slots with `is_booked = TRUE` will never be removed except if the current time is after their end time."""

    # Set up timezone
    paris_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(paris_tz)
    end_time = now + timedelta(hours=46)        # When you want you're last time_slot from current time
    interval = timedelta(hours=2)  # Time slot interval (2 hours) between each unique time_slot

    # Align current time to the nearest previous hour
    start_time = now.replace(minute=0, second=0, microsecond=0)

    pool = container.get_pool()
    if pool:
        connection = None
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:

                    """Delete old table rows, where time-slot has ended."""
                    delete_old_slots_query = """
                        DELETE FROM time_slots 
                        WHERE end_time < %s
                    """
                    await cursor.execute(delete_old_slots_query, (now,))

                    # Insert new time slots within the next 46 hours
                    while start_time + interval <= end_time:
                        end_time_slot = start_time + interval

                        # Insert new time slot only if it does not exist
                        query_insert = """
                            INSERT INTO time_slots (start_time, end_time, is_booked) 
                            VALUES (%s, %s, FALSE)
                            ON CONFLICT (start_time, end_time) 
                            DO NOTHING
                        """
                        await cursor.execute(query_insert, (start_time, end_time_slot))

                        # Move to the next slot
                        start_time = end_time_slot

                    logger.info("Time slots populated successfully.")

        except Exception as e:
            logger.error(f"Error during database operations: {e}", exc_info=True)

        finally:
            if connection:
                await return_cursor_connection_to_pool(connection)
    else:
        logger.error("Database connection pool is not available.")