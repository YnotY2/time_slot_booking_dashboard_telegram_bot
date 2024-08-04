from datetime import datetime, time
import pytz


"""Define active hours of the bot. Openings hours for coffee shop is from 8:00-22:00"""
def check_if_time_within_openings_hours(start_hour=0, start_minute=0, end_hour=23, end_minute=59, tz_name='Europe/Paris'):
    # Define the timezone
    tz = pytz.timezone(tz_name)
    # Get the current time in UTC and convert to the specified timezone
    now = datetime.now(pytz.utc).astimezone(tz).time()

    # Define the start and end times in the specified timezone
    start_time = time(start_hour, start_minute)  # Start time (e.g., 8:00 )
    end_time = time(end_hour, end_minute)  # End time (e.g., 23:00 PM)

    """ Check if the current time is within the allowed time window
    # Returns True if between times otherwise returns False."""
    return start_time <= now <= end_time


if __name__ == "__main__":
    check_if_time_within_openings_hours()