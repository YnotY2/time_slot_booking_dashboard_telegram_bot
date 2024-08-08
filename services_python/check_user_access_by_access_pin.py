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
    """Check if the PIN is valid based on current time and perform actions accordingly.
    We return a dict with the exact auth results"""

    # Initialize the timezone and get the current time
    paris_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(paris_tz)

    # Initialize variables
    pin_inside_time_slot = None
    pin_outside_time_slot = None
    pin_valid = None
    start_time = None
    end_time = None

    pool = container.get_pool()
    if pool:
        try:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Check if the PIN exists in the time_slots table
                    query_check_pin = """
                        SELECT start_time, end_time
                        FROM time_slots
                        WHERE access_pin = %s
                    """
                    await cursor.execute(query_check_pin, (access_pin,))
                    row = await cursor.fetchone()

                    if row:
                        pin_valid = True
                        start_time, end_time = row  # unpack the result row

                        # Convert start_time and end_time to timezone-aware datetimes if they are naive
                        if start_time.tzinfo is None:
                            start_time = paris_tz.localize(start_time)
                        if end_time.tzinfo is None:
                            end_time = paris_tz.localize(end_time)

                        # Check if current time is within the time slot
                        if start_time <= now <= end_time:
                            logger.info("PIN is valid and within the time slot.")
                            pin_inside_time_slot = True
                            # Continue with your logic for valid time slot
                        else:
                            logger.info(f"PIN valid, but outside of time slot. Wait till exactly: {start_time}")
                            # Optionally, wait or trigger a different action
                            pin_outside_time_slot = True

                    else:
                        logger.info("PIN not found.")
                        pin_valid = False

        except Exception as e:
            logger.error(f"Error during database operations: {e}")

        finally:
                # Here we return the dict:
                user_access_auth_return_data = {
                    'pin': pin_valid,
                    'pin_inside_time_slot': pin_inside_time_slot,
                    'pin_outside_time_slot': pin_outside_time_slot,
                    'start_time': start_time,
                    'end_time': end_time

                }
                await return_cursor_connection_to_pool(cursor)
                logger.info("Successfully returned the connection to the pool!")
                logger.info(f"Returning 'user_access_auth_return_data'")
                return user_access_auth_return_data
    else:
        logger.error("Database connection pool is not available.")