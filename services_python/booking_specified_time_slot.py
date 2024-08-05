import asyncio

from utils.colors import Colors
from utils.logger import setup_logger

from services_python.return_cursor_connection_to_pool import return_cursor_connection_to_pool
from services_python.fetch_time_slot_row_by_id import fetch_time_slot_row_by_id

# Set up logger with service name
service_name = "booking_specified_time_slot"
logger = setup_logger(service_name)


async def booking_specified_time_slot(callback):
    async def extract_time_slot(callback_data):
        # Assuming callback_data is in the format 'confirm_buy_{time_slot_id}'
        parts = callback_data.split('_')

        if len(parts) > 2:
            return parts[-1]
        else:
            raise ValueError("Callback data format is incorrect")

    try:
        # Extract time_slot_id from callback data
        time_slot_id = await extract_time_slot(callback.data)

        # Fetch time slot data from the database
        time_slot_data = await fetch_time_slot_row_by_id(time_slot_id)

        if not time_slot_data:
            raise ValueError("Time slot data not found")

        # Access start_time and end_time from the dictionary
        start_time = time_slot_data['start_time']
        end_time = time_slot_data['end_time']

        # Ensure these are strings for rstrip to work
        start_time_str = str(start_time)
        end_time_str = str(end_time)

        # Remove the '.00' suffix if it exists
        start_time_cleaned = start_time_str.rstrip('.00')
        end_time_cleaned = end_time_str.rstrip('.00')

        # Define the message
        message = (
            f"\n"
            " ✅ Time slot confirmed:\n"
            f"\n"
            f"Start-Time:       🗓️ {start_time_cleaned}\n"
            f"End-Time:         🗓️ {end_time_cleaned}\n"
            f"\n"
            "Please message the following admin: @handle\n"
            "Copy this message below and send it to continue with payment:\n"
            "\n"
            "```"
            "Hi, I would like to confirm my access to the [service]\n"  
            "\n" 
            f"Start-Time:       🗓️ {start_time_cleaned}\n"
            f"End-Time:         🗓️ {end_time_cleaned}\n"
            f"\n"
            f"Time-slot-ID:     📒 {time_slot_id}"
            "\n"  
            "🪐 I acknowledge that I am sending this message \n"  
            "to book the [service] for above specified time-slot\n"  # No trailing newline
            "```"
            f"\n"
            f"ℹ️ Dear user, after you have sent this message to "
            f"@handle. You will receive a message response from @handle"
            f" within the chat you sent the message to.\n"
            f"\n"
            f"🚀 Please be patient while waiting for response... "
        )

        # Send the message
        await callback.message.answer(message, parse_mode='MarkDown')

        # Here we sleep 2min, so the user can send the message before being shown the order-recap msg
        # Simulate some asynchronous work with a delay

    except ValueError as e:
        logger.error(f"Value error: {e}", exc_info=True)
        await callback.message.answer(f"Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        await callback.message.answer("An unexpected error occurred. Please try again later.")
