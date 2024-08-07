"""This function will query database to find available time slots for user to book.
We return the found time-slots in a dict with each time slot data."""


from datetime import datetime, timedelta
import pytz

from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "fetch_all_available_time_slots"
logger = setup_logger(service_name)


async def fetch_all_available_time_slots():
    """Fetch available time slots that are between 2 hours and 46 hours from now, in reverse order."""

    # Initialize the list to store available time slots
    available_time_slots = []

    # Set up timezone
    paris_tz = pytz.timezone('Europe/Paris')

    # Calculate the current time and the time boundaries
    now = datetime.now(paris_tz)
    start_window = now + timedelta(hours=0)  # Start time is 0 hours from now
    end_window = now + timedelta(hours=46)  # End time is 46 hours from now

    pool = container.get_pool()
    if pool:
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Query to fetch available time slots within the defined range, ordered by start time in descending order
                    query_fetch_slots = """
                        SELECT id, start_time, end_time 
                        FROM time_slots 
                        WHERE is_booked = FALSE
                          AND start_time >= %s
                          AND start_time < %s
                        ORDER BY start_time DESC
                    """
                    await cursor.execute(query_fetch_slots, (start_window, end_window))
                    results = await cursor.fetchall()

                    if not results:
                        logger.info("No available time slots found within the specified range.")
                        return available_time_slots

                    # Process the results
                    for row in results:
                        slot_id, start_time, end_time = row
                        available_time_slots.append({
                            'id': slot_id,
                            'start_time': start_time,
                            'end_time': end_time
                        })

                    logger.info("Successfully fetched available time slots.")

        except Exception as e:
            logger.info(f"Error during database operations: {e}")

        finally:
            await return_cursor_connection_to_pool(connection)
            logger.info("Successfully returned the cursor and connection to the pool!")
            return available_time_slots
    else:
        logger.error("Database connection pool is not available.")
        return available_time_slots