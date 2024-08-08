import asyncio

from utils.colors import Colors
from utils.logger import setup_logger

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Set up logger with service name
service_name = "authentication_response_message_access_pin"
logger = setup_logger(service_name)


async def authentication_response_message_access_pin(callback, user_access_auth_return_data):
    try:
        # Here we attempt to extract the values from the dict
        pin_valid = user_access_auth_return_data['pin_valid']
        start_time = user_access_auth_return_data['start_time']
        end_time = user_access_auth_return_data['end_time']
        pin_outside_time_slot = user_access_auth_return_data['pin_outside_time_slot']
        pin_inside_time_slot = user_access_auth_return_data['pin_inside_time_slot']

    except Exception as e:
        logger.error(f"Error extracting the variables values from the dict: {e}")

    # Convert the time variables for better readability
    # Remove the '.00' suffix if it exists
    # Only tim the time if it actually has a value
    # Convert the datetime objects to strings with proper formatting
    if start_time:
        start_time_cleaned = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_cleaned = end_time.strftime('%Y-%m-%d %H:%M:%S')

    if pin_valid and pin_inside_time_slot:
        # Define the message
        message = (
            f"\n"
            " ✅ Access confirmed:\n"
            "\n"
            f"Start-Time:       🗓️ {start_time_cleaned}\n"
            f"End-Time:         🗓️ {end_time_cleaned}\n"
            f"\n"
            f"ℹ️ Dear user, we thank you for trusting"
            f"our [service] . And we will deliver the best"
            f"service we can offer. "
            f"\n"
            f"🚀 "
        )
    elif pin_valid and pin_outside_time_slot:
        # Define the message
        message = (
            f"\n"
            "✖️ Access denied:\n"
            "\n"
            f"Start-Time:       🗓️ {start_time_cleaned}\n"
            f"\n"
            f"End-Time:         🗓️ {end_time_cleaned}\n"
            f"\n"
            f"ℹ️ Dear user, the access PIN you have entered"
            f"is valid. But you are attempting to access service"
            f" outside of booked time-slot.\n"
            f"\n"
            f"View above booking time, for when you can access service ⬆️"
            f"\n"
            f"🚀 "
        )
    elif not pin_valid:   # if the PIN is not valid
        message = (
            f"\n"
            "✖️ Access denied:\n"
            "\n"
            f"ℹ️ Dear user, the access PIN you have entered"
            f"is not valid. You have either entered the wrong PIN"
            f" or have not yet booked a time-slot.\n"
            f"\n"
            f"🗓 To book a time-slot press the 'Booking Service' button.️"
            f"\n"
            f"🚀 "
        )

    # Define the keyboard for if a user has entered wrong PIN, or outside of time:
    faq_menu_button = types.InlineKeyboardButton(text="FAQ", callback_data='faq_menu')
    booking_service_button = InlineKeyboardButton(text="Booking Service", callback_data='booking_service')
    start_menu_button = types.InlineKeyboardButton(text="Back to Main Menu", callback_data='start')

    # Create an InlineKeyboardMarkup object with a list of rows
    auth_response_inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [faq_menu_button, booking_service_button],
            [start_menu_button], # Second row
        ]
    )

    # Here we either send response with keyboard buttons or not
    if not pin_valid and pin_outside_time_slot:
        await callback.message.answer(message, reply_markup=auth_response_inline_keyboard)
    elif not pin_valid and pin_inside_time_slot:
        await callback.message.answer(message, reply_markup=auth_response_inline_keyboard)
    elif not pin_valid and not pin_inside_time_slot:
        await callback.message.answer(message, reply_markup=auth_response_inline_keyboard)
    elif pin_valid and pin_outside_time_slot:
        await callback.message.answer(message, reply_markup=auth_response_inline_keyboard)

    # If we reach here we have successfully accessed the service with valid pin and time-window
    elif pin_valid and pin_inside_time_slot:
        await callback.message.answer(message)
