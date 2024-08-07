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
    """Populate the database with time slots for the next 46 hours, refreshing as needed.
    Must be at least one end_time within time_slots row; this decides if the time_slots
    are available on even or odd numbers.
    """

    """INSERT INTO time_slots (start_time, end_time, is_booked)
VALUES ('2024-08-<start_int_day> 10:00:00', '2024-<end_int_day>-08 12:00:00', FALSE);
"""

    # Set up timezone
    paris_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(paris_tz)
    end_time = now + timedelta(hours=46)
    interval = timedelta(hours=2)

    pool = container.get_pool()
    if pool:
        connection = None
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                        try:
                            # Find the latest existing slot's end time
                            latest_slot_query = """
                                                           SELECT MAX(end_time) FROM time_slots
                                                       """
                            await cursor.execute(latest_slot_query)
                            latest_slot_row = await cursor.fetchone()

                            # Ensure timezone-awareness for latest_slot_end_time
                            latest_slot_end_time = latest_slot_row[0] if latest_slot_row[0] else None
                            if latest_slot_end_time:
                                if latest_slot_end_time.tzinfo is None:
                                    latest_slot_end_time = paris_tz.localize(latest_slot_end_time)
                            else:
                                latest_slot_end_time = now

                            # Align latest_slot_end_time to the nearest future interval if necessary
                            if latest_slot_end_time < now:
                                latest_slot_end_time = now
                            else:
                                latest_slot_end_time = (latest_slot_end_time + interval - timedelta(seconds=1)).replace(
                                    minute=0, second=0, microsecond=0)

                            # Generate time slots from the latest existing slot or now
                            start_time = latest_slot_end_time
                            time_slots_to_insert = []
                            while start_time + interval <= end_time:
                                end_time_slot = start_time + interval
                                time_slots_to_insert.append((start_time, end_time_slot))
                                start_time = end_time_slot

                            # Insert new time slots only if they do not already exist
                            query_insert = """
                                                           INSERT INTO time_slots (start_time, end_time, is_booked) 
                                                           SELECT %s, %s, FALSE
                                                           WHERE NOT EXISTS (
                                                               SELECT 1 FROM time_slots
                                                               WHERE start_time = %s AND end_time = %s
                                                           )
                                                       """
                            for start, end in time_slots_to_insert:
                                await cursor.execute(query_insert, (start, end, start, end))

                            # Remove old slots where end_time is before now and they are not booked
                            delete_old_slots_query = """
                                                           DELETE FROM time_slots 
                                                           WHERE end_time < %s AND is_booked = FALSE
                                                       """
                            await cursor.execute(delete_old_slots_query, (now,))
                            logger.info("Time slots populated successfully.")

                        except Exception as e:
                            logger.error(f"Error during database operations: {e}", exc_info=True)

        except Exception as e:
            logger.error(f"Error acquiring connection from pool: {e}", exc_info=True)

        finally:
            if connection:
                await return_cursor_connection_to_pool(connection)
    else:
        logger.error("Database connection pool is not available.")