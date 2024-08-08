"""This function will take the user's given 'access_pin' they received when
after Admin has given it to them. This pin corresponds to a booking ID"""


from datetime import datetime
import pytz

from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from dependencies import container

# Set up logger with service name
service_name = "check_user_access_by_access_pin"
logger = setup_logger(service_name)


async def check_user_access_by_access_pin(access_pin: str):
    """Check if the PIN is valid based on current time and perform actions accordingly."""

    # Initialize the timezone and get the current time
    paris_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(paris_tz)

    pool = container.get_pool()
    if pool:
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Check if the PIN exists in the confirmed_orders table
                    query_check_pin = """
                            SELECT start_time, end_time, is_booked
                            FROM time_slots
                            WHERE access_pin = %s
                        """
                    await cursor.execute(query_check_pin, (access_pin,))
                    row = await cursor.fetchone()

                    if row:
                        start_time, end_time = row  # unpack the result row

                        # Check if current time is within the time slot
                        if start_time <= now <= end_time:
                            logger.info("PIN is valid and within the time slot.")
                            # Continue to use functions as required

                        else:
                            # PIN is valid but outside of the time slot
                            logger.info(f"PIN valid, but outside of time slot. Wait till exactly: {start_time}")
                            # Optionally, wait or trigger a different action

                    else:
                        logger.info("PIN not found.")

        except Exception as e:
            logger.error(f"Error during database operations: {e}")

        finally:
                await return_cursor_connection_to_pool(cursor)
                logger.info("Successfully returned the connection to the pool!")
    else:
        logger.error("Database connection pool is not available.")