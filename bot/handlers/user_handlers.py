# This user_handlers file basically handles all incoming message's callback data and real logic of the
# Telegram bot it's self. If I want to call a function responding to a callback_data I do it here.
# Bot should only respond to direct messages.
import asyncio

from aiogram import Router, types
from aiogram.filters import Command

from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.faq_answers import faq_answers
from config.faq_data import faq_data
from config.settings import start_menu_image_logo
from config.settings import how_is_our_coffee_made_video
from config.settings import who_are_we_video
from config.settings import admin_manage_bookings_dashboard_password

from services_python.check_if_time_within_openings_hours import check_if_time_within_openings_hours

from services_python.fetch_all_available_time_slots import fetch_all_available_time_slots
from services_python.fetch_all_time_slots import fetch_all_time_slots
from services_python.fetch_time_slot_row_by_id import fetch_time_slot_row_by_id
from services_python.booking_specified_time_slot_user_message import booking_specified_time_slot_user_message
from services_python.manage_booking_time_slots import manage_booking_time_slots

"""These are imports used for development purposes."""
#from services_python.test_pool_object_from_user_handler import test_pool_object_from_user_handler

from utils.colors import Colors
from utils.logger import setup_logger
logger = setup_logger(service_name="user_handlers")


"""Initiate the router from aiogram library, for handling user events."""
user_router = Router()


"""Define the handler for unexpected messages, reply to any except 'start'"""
@user_router.message()
async def handle_unexpected_message(message: types.Message):
    response_message = None  # Default to None to indicate no response by default

    try:
        if message.text.startswith('/'):    # We know if user is attempting a cmd
            command = message.text.split()[0]
            """Handle all message's actions/response for message's outside of button interactions."""

            """This command will give user's/admin access to dashboard for booking/un-booking time-slots."""
            if command == admin_manage_bookings_dashboard_password:
                response_message = ("✨ Admin dashboard\n"
                                    "\n"
                                    "📘 Managing time-slots bookings.")
                # Here we call the dashboard
                await admin_time_slot_booking_dashboard(message)


            # This is the only command actually used by normal users, outside of the buttons.
            elif command == '/start':
                await start_menu(message)
                return  # Exit early to avoid sending a message

            # Handle unknown commands
            else:
                response_message = ("ℹ️ Unknown command. Please use the buttons provided to interact with the bot.\n"
                                    "\n"
                                    "Or bring up Main-Menu with 🚀 '/start'")
        # Handle unknown message
        else:
            response_message = ("ℹ️ Please use the buttons provided to interact with the bot.\n"
                                "\n"
                                "Or bring up Main-Menu with 🚀 '/start'")

    except Exception as e:
        logger.error(f"{Colors.RED}Error during 'handle_unexpected_message' operations: {e}.{Colors.END}")
        response_message = "An error occurred. Please try again later."

    finally:
        if response_message:
            await message.answer(text=response_message)



"""This is the only command received from the user, all other data is callback data."""
@user_router.message(Command('start'))
async def start_menu(message: types.Message):
    # The "None" message being sent has nothing to do with the start_menu function.

    """Check if message is received between openings hours"""
    if not check_if_time_within_openings_hours():
        await message.answer("Sorry, 🕣\n"
                             "\n"
                             "The shop is only available between:\n"
                             "8:00 - 23:50 | EU UTC+2. ")
        return

    faq_button = InlineKeyboardButton(text="FAQ", callback_data='faq_menu')
    buy_button = InlineKeyboardButton(text="Buy", callback_data='buy')
    who_are_we_button = InlineKeyboardButton(text="Who are we?", callback_data="who_are_we")

    # Create an InlineKeyboardMarkup object with a list of rows
    start_keyboard_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [faq_button],         # First row
            [buy_button],  # Second row
            [who_are_we_button],  # Third row

        ]
    )

    photo = FSInputFile(start_menu_image_logo, filename="start_menu_image_logo.png")

    # Send the photo with caption and inline keyboard
    await message.answer_photo(
        photo=photo,
        caption=(
            '☕ 𝙲𝚒𝚒𝚏𝚎  𝙲𝚘𝚏𝚏𝚎𝚎  \n'
            '\n'
            '☕ We provide the quick and most delicious coffee. \n'
            '\n'
            'Welcome! Please choose an option 🌟 :\n'
            '\n'
            '🌑 Have any other questions? Click "FAQ" \n'
            '🌑 If you want to purchase your coffee, click "Buy Coffee"\n'
            '\n'
            'Pricing: \n'
            '3,50€ 💶'
        ),
        reply_markup=start_keyboard_inline
    )


async def show_faq_options(callback: types.CallbackQuery):
    rows = [[InlineKeyboardButton(text=question, callback_data=key)] for key, question in faq_data.items()]
    rows.append([InlineKeyboardButton(text="Back to Main Menu", callback_data='start')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)

    if callback.message.text:
        await callback.message.edit_text(text="Choose a question:", reply_markup=keyboard)
    else:
        await callback.message.answer(text="Choose a question:", reply_markup=keyboard)


async def back_to_faq_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to FAQ", callback_data='faq_menu')],
            [InlineKeyboardButton(text="Back to Main Menu", callback_data='start')]
        ]
    )
    return keyboard


# This functions will send the video for the answer
async def handle_how_is_our_coffee_made_faq_answer(callback: types.CallbackQuery):
    try:
        # Create an FSInputFile object for the video
        video = FSInputFile(how_is_our_coffee_made_video, filename="how_is_our_coffee_made_video.mp4")
        # Here we define the message:
        message = ("\n"
                   "❤️ Our Coffee Is made with love and care :\n"
                   "\n")

        faq_menu_button = types.InlineKeyboardButton(text="FAQ", callback_data='faq_menu')
        start_menu_button = types.InlineKeyboardButton(text="Back to Main Menu", callback_data='start')

        # Create an InlineKeyboardMarkup object with a list of rows
        back_inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [faq_menu_button, start_menu_button],  # Second row
            ]
        )
        # Send the local video file and FAQ information
        await callback.message.answer_video(
            video=video,
            caption=message,
            reply_markup=back_inline_keyboard
        )

    except Exception as e:
        # Handle exceptions if the bot is blocked or the chat is not found
        print(f"Error sending video 'how_is_our_coffee_made_video' : {e}")


# This functions will send the video for the answer
async def handle_who_are_we_answer_faq_answer(callback: types.CallbackQuery):
    try:
        # Create an FSInputFile object for the video
        video = FSInputFile(who_are_we_video, filename="who_are_we.mp4")
        # Here we define the message:
        message = ("\n"
                   "⛓️ This is who we are :\n"
                   "\n")

        faq_menu_button = types.InlineKeyboardButton(text="FAQ", callback_data='faq_menu')
        start_menu_button = types.InlineKeyboardButton(text="Back to Main Menu", callback_data='start')

        # Create an InlineKeyboardMarkup object with a list of rows
        back_inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [faq_menu_button, start_menu_button],  # Second row
            ]
        )
        # Send the local video file and FAQ information
        await callback.message.answer_video(
            video=video,
            caption=message,
            reply_markup=back_inline_keyboard
        )
    except Exception as e:
        print(f"Error sending video 'who_are_we': {e}")

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def callback_handler_buy(callback: types.CallbackQuery):
    """Handle the callback query to display time slots and additional buttons.
    This displays the time-slots booking GUI, when 'buy' button is pressed."""

    # Create time slot buttons
    async def create_time_slot_buttons(available_time_slots):
        # Check if the dictionary results is not empty.
        if not available_time_slots:
            return None  # Return None when there are no slots available

        keyboard = []
        for i, slot in enumerate(available_time_slots):
            # Format to show only day and time
            start_time_str = slot['start_time'].strftime("%d %H:%M")
            end_time_str = slot['end_time'].strftime("%H:%M")
            button_text = f"{start_time_str} - {end_time_str}"
            callback_data = f"time_slot_{slot['id']}"
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)

            # Add the button to a row
            if i % 2 == 0:
                # Start a new row
                keyboard.append([button])
            else:
                # Add to the last row
                keyboard[-1].append(button)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Create the buttons
    faq_button = InlineKeyboardButton(text='FAQ', callback_data='faq_menu')
    start_menu_button = InlineKeyboardButton(text="Back to Main Menu", callback_data='start')

    # Fetch available time slots from the database
    available_time_slots = await fetch_all_available_time_slots()
    print(available_time_slots)

    # Call above function and generate the time slot buttons, pass 'available_time_slots' variable
    time_slot_buttons = await create_time_slot_buttons(available_time_slots)

    """if not available time-slots within the database table, after populating"""
    if time_slot_buttons is None:
        message = ("⌛ No time slots available at this time...\n"
                   "\n"
                   "Please check again in 2 hours ⌚\n")

        # Create an InlineKeyboardMarkup object with a list of rows
        back_inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [start_menu_button, faq_button],  # Second row
            ]
        )

        await callback.message.answer(text=message, reply_markup=back_inline_keyboard)
        return

    """Here we send the time-slots and there corresponding callback-data."""
    # Add the "FAQ" and "Back to Main Menu" buttons to the keyboard
    inline_keyboard = time_slot_buttons.inline_keyboard  # Existing time slot buttons
    inline_keyboard.append([faq_button, start_menu_button])  # Add the new buttons to the end

    # Create the InlineKeyboardMarkup object with all buttons
    full_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    # Send the message with the updated keyboard
    message = ("⌛ Please select a time slot below ⬇️ \n"
               "\n"
               "[ 🗓️ day | start ⌚ | end ⌚ ]\n")
    await callback.message.answer(text=message, reply_markup=full_inline_keyboard)

    message = ("⌛ Please select a above time slot 🔼 :")
    await callback.message.answer(message)



async def process_selected_time_slot(callback: types.CallbackQuery):
    # You can fetch or process the selected time slot based on the ID
    # Extract callback data
    callback_data = callback.data

    if callback_data.startswith('time_slot_'):
        # Remove the prefix 'time_slot_' to get the ID
        time_slot_id = callback_data[len('time_slot_'):]

        # Convert to integer if needed
        time_slot_id = int(time_slot_id)
        time_slot_data = await fetch_time_slot_row_by_id(time_slot_id)
        print(time_slot_data)

        # Access start_time and end_time from the dictionary
        start_time = time_slot_data['start_time']
        end_time = time_slot_data['end_time']

        # Ensure these are strings for rstrip to work
        start_time_str = str(start_time)
        end_time_str = str(end_time)

        # Remove the '.00' suffix if it exists
        start_time_cleaned = start_time_str.rstrip('.00')
        end_time_cleaned = end_time_str.rstrip('.00')

        # Here we define the message:
        message = ("\n"
                   " ⌛ Confirm Time Slot :\n"
                   "\n"
                   f"Start-Time:    🗓️ {start_time_cleaned}\n "
                   f"\n"
                   f"End-Time:   ️    🗓 {end_time_cleaned}\n"
                   f"\n")

        start_menu_button = types.InlineKeyboardButton(text="Back to Main Menu", callback_data='start')
        buy_button = types.InlineKeyboardButton(text='Confirm Time', callback_data=f'confirm_buy_{time_slot_id}')
        # We pass the time-slot ID to the callback data of confirm buy, so we can
        # now what time-slot the user is talking about.

        # Create an InlineKeyboardMarkup object with a list of rows
        confirm_buy_inline_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [start_menu_button, buy_button],  # Second row
            ]
        )

    else:
        # Here we define the message:
        message = ("\n"
                   " Time slot is no longer available, sorry! :\n"
                   "\n"
                   "")

    # Here we call the response
    await callback.message.answer(message, parse_mode='Markdown', reply_markup=confirm_buy_inline_keyboard)


async def order_recap_customer_message(callback: types.CallbackQuery, status: bool):
    await asyncio.sleep(120)  # Sleep for 2 seconds to simulate processing

    faq_menu_button = types.InlineKeyboardButton(text="FAQ", callback_data='faq_menu')
    start_menu_button = types.InlineKeyboardButton(text="Back to Main Menu", callback_data='start')

    # Create an InlineKeyboardMarkup object with a list of rows
    finished_order_inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [faq_menu_button, start_menu_button],  # Second row
        ]
    )

    if status:
        message = (
            "🧾\n"
            "\n"
            "🚀 Dear Customer,\n"
            "Thank you for your order. \n"
            "Please wait for a response from '@handle'"
            "\n"
        )
    else:
        message = (
            "🧾\n"
            "\n"
            "🚀 Dear Customer,\n"
            "Order Failed. \n"
            "\n"
            "📉 Money not received.\n"
            "\n"
            '🌱 This is because you failed to pay'
            ' for the coffee after a certain amount of time.'
            "📜 We are sorry that this happened. Please try again."
        )

    # Send the message using bot instance
    await callback.message.answer(message, parse_mode='Markdown', reply_markup=finished_order_inline_keyboard)



async def admin_time_slot_booking_dashboard(message: types.Message):
    """Handle the callback query to display time slots managing dashboard.
    We can choose a time-slot then call 'admin_managing_time_slot_bookings' to manage it."""

    async def create_time_slot_buttons(available_time_slots):
        # Check if the dictionary results is not empty.
        if not available_time_slots:
            return None  # Return None when there are no slots available

        keyboard = []
        for i, slot in enumerate(available_time_slots):
            # Format to show only day and time
            start_time_str = slot['start_time'].strftime("%d %H:%M")
            end_time_str = slot['end_time'].strftime("%H:%M")
            button_text = f"{start_time_str} - {end_time_str}"
            callback_data = f"admin_manage_booking_time_slot_{slot['id']}"
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)

            # Add the button to a row
            if i % 2 == 0:
                # Start a new row
                keyboard.append([button])
            else:
                # Add to the last row
                keyboard[-1].append(button)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    # !!!!!!!!!!!!!!!!!!!!!!!!!
    # Fetch available time slots from the database, we need to fetch all time-slots not just available.
    all_time_slots = await fetch_all_time_slots()
    logger.info(all_time_slots)

    # Call above function and generate the time slot buttons, pass 'available_time_slots' variable
    time_slot_buttons = await create_time_slot_buttons(all_time_slots)

    if time_slot_buttons is None:
        # Message when no time slots are available
        message_text = (
            "⌛ No time slots available at this time...\n"
            "\n"
            "Please check again in 2 hours ⌚\n"
        )
        await message.answer(text=message_text)
        return  # Exit early as there are no time slots available

    # Add the "FAQ" and "Back to Main Menu" buttons to the keyboard
    inline_keyboard = time_slot_buttons.inline_keyboard  # Existing time slot buttons
    # Create the InlineKeyboardMarkup object with all buttons
    full_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    # Send the message with the updated keyboard
    message_text = (
        "⌛ Please select a time slot below ⬇️ \n"
        "\n"
        "[ 🗓️ day | start ⌚ | end ⌚ ]\n"
    )
    await message.answer(text=message_text, reply_markup=full_inline_keyboard)

    # Additional message prompting user to select a time slot
    additional_message_text = (
        "⌛ Please select a time slot above 🔼 :\n"
    )
    await message.answer(text=additional_message_text)


async def admin_managing_specified_time_slot_booking_choose_true_false(callback: types.CallbackQuery):
    """This functions gives capability to specify if time_slot should be True or False"""
    async def extract_time_slot(callback_data):
        # Assuming callback_data is in the format 'confirm_buy_{time_slot_id}'
        parts = callback_data.split('_')

        if len(parts) > 2:
            return parts[-1]
        else:
            raise ValueError("Callback data format is incorrect")

    # Extract time_slot_id from callback data
    time_slot_id = await extract_time_slot(callback.data)
    # FROM HERE TILL

    # Here we have successfully done our database operation
    time_slot_data = await fetch_time_slot_row_by_id(time_slot_id)

    # Access start_time and end_time from the dictionary
    start_time = time_slot_data['start_time']
    end_time = time_slot_data['end_time']
    is_booked = time_slot_data['is_booked']
    access_pin = time_slot_data['access_pin']

    # Ensure these are strings for rstrip to work
    start_time_str = str(start_time)
    end_time_str = str(end_time)
    is_booked_str = str(is_booked)
    access_pin_str = str(access_pin)

    # Remove the '.00' suffix if it exists
    start_time_cleaned = start_time_str.rstrip('.00')
    end_time_cleaned = end_time_str.rstrip('.00')

    message = (
        f"🚀 Dear Admin,\n"
        f"\n"
        f"🗓 Manage specified booking time-slot:\n"
        f"\n"
        f"\n" 
        f"Start-Time:       🗓️ {start_time_cleaned}\n"
        f"End-Time:         🗓️ {end_time_cleaned}\n"
        f"\n"
        f"Time-slot-ID:     📒 {time_slot_id}"
        f"👓 'is_booked'  =    {is_booked_str}"
        f"\n"
        f"Access PIN 📲  {access_pin_str}\n"       
        f"\n"
    )

    faq_menu_button = types.InlineKeyboardButton(text="Book-Time-Slot", callback_data=f'admin_managing_specified_time_slot_booking_True_{time_slot_id}')
    start_menu_button = types.InlineKeyboardButton(text="Un-Book-Time-Slot", callback_data=f'admin_managing_specified_time_slot_booking_False_{time_slot_id}')

    # Create an InlineKeyboardMarkup object with a list of rows
    admin_managing_specified_time_slot_booking_choose_true_false_inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [faq_menu_button, start_menu_button],  # Second row
        ]
    )

    # HERE ADDING 'access_pin_str' and 'is_booked_str' broke the code.
    # Send the message using bot instance
    await callback.message.answer(message, reply_markup=admin_managing_specified_time_slot_booking_choose_true_false_inline_keyboard)


async def admin_modify_time_slot_booking_status(callback: types.CallbackQuery):
    """This function takes care of booking or un-book time-slot
    . by time-slot ID. capability to set 'is_booked' = True/False"""

    # This function takes callback_data and either books or un-books time-slot
    logger.info(f"We made it to 'admin_modify_time_slot_booking_status'")
    async def extract_time_slot_and_action(callback_data):
        # Split the callback data based on underscores
        parts = callback_data.split('_')

        # Ensure the callback data has at least the required number of parts
        if len(parts) >= 4:
            # Extract the time slot ID from the last part
            time_slot_id = parts[-1]

            # Extract the booking action from the second last part and convert to boolean
            action = parts[-2].lower()  # 'True' or 'False'
            book_time_slot = action == 'true'  # Convert to boolean
            return time_slot_id, book_time_slot

        else:
            # Raise an error if the callback data format is incorrect
            raise ValueError("Callback data format is incorrect")

    # Extract time_slot_id from callback data
    time_slot_id, book_time_slot = await extract_time_slot_and_action(callback.data)

    response, access_pin = await manage_booking_time_slots(time_slot_id, book_time_slot)

    try:
        # Here we have successfully done our database operation
        time_slot_data = await fetch_time_slot_row_by_id(time_slot_id)

        # Access start_time and end_time from the dictionary
        start_time = time_slot_data['start_time']
        end_time = time_slot_data['end_time']
        is_booked = time_slot_data['is_booked']
        access_pin = time_slot_data['access_pin']

        # Ensure these are strings for rstrip to work
        start_time_str = str(start_time)
        end_time_str = str(end_time)
        is_booked_str = str(is_booked)
        access_pin_str = str(access_pin)

        # Remove the '.00' suffix if it exists
        start_time_cleaned = start_time_str.rstrip('.00')
        end_time_cleaned = end_time_str.rstrip('.00')

        message_modification_result = (
            f"🚀 Dear Admin,\n"
            f"\n"
            f"✅ Successfully modified following time-slot:\n"
            f"\n"
            f"Start-Time:       🗓️ {start_time_cleaned}\n"
            f"End-Time:         🗓️ {end_time_cleaned}\n"
            f"\n"
            f"Time-slot-ID:     📒 {time_slot_id}\n"
            f"👓 'is_booked'  =    {is_booked_str}"
            f"\n"
            f"Access PIN 📲  `{access_pin_str}`\n"
            f"\n"
        )

        if response:
            faq_menu_button = types.InlineKeyboardButton(text="FAQ", callback_data='faq_menu')
            start_menu_button = types.InlineKeyboardButton(text="Back to Main Menu", callback_data='start')

            # Create an InlineKeyboardMarkup object with a list of rows
            finished_order_inline_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [faq_menu_button, start_menu_button],  # Second row
                ]
            )

            # Send the message using bot instance
            await callback.message.answer(message_modification_result, reply_markup=finished_order_inline_keyboard)

            # Send a follow up message containing data you would send to user
            message = (
                F"If you wish to send access to the user, do that with"
                F"this following message:\n"
                F"\n"
                "```"
                f"\n"
                "✅ Time slot payment complete.\n"
                f"🔓 Access information to service:\n"
                f"\n"
                f"Start-Time:       🗓️ {start_time_cleaned}\n"
                f"End-Time:         🗓️ {end_time_cleaned}\n" 
                f"Access PIN 📲     {access_pin_str}\n"
                f"\n"
                f"ℹ️ Dear user, to be able to use the service from start-time till end-time. "
                f"You need to enter the above access "
                f"pin within the key-pad lock"
                f" that show's up when clicking 'access' button within Main-Menu.\n"
                f"\n"
                f"🚀 Thank you for you're purchase!\n"
                "🪐 If you have any questions, message us: @handle \n"  
                "```"
            )
            await callback.message.answer(message, parse_mode='MarkDown')

        elif not response:
            # Send a follow up message containing data you would send to user
            await callback.message.answer(text=message_modification_result)

        elif response == None:
            await callback.message.answer(text=f"Time slot {time_slot_id} was not booked or already unbooked. ")
            logger.info(f"Time slot {time_slot_id} was not booked or already unbooked. ")


    except Exception as e:
        logger.info(f"Error running 'manage_booking_time_slots'.: {e} ")
        await callback.message.answer(text=f"Error running 'manage_booking_time_slots'. ")



@user_router.callback_query()
async def handle_callback_query(callback: types.CallbackQuery):
    try:
        if not check_if_time_within_openings_hours():
            await callback.message.answer(
                                 "Sorry, 🕣\n"
                                 "\n"
                                 "The shop is only available between:\n"
                                 "8:00 - 23:50 | EU UTC+2. ")
            return

        data = callback.data

        if data == 'faq_menu':
            await show_faq_options(callback)
        elif data.startswith('faq_'):
            question_id = data
            if question_id in faq_answers:
                answer = faq_answers[question_id]
                reply_markup = await back_to_faq_keyboard()  # Await the function to get the InlineKeyboardMarkup
                await callback.message.edit_text(text=answer, reply_markup=reply_markup)
            else:
                reply_markup = await back_to_faq_keyboard()  # Await the function to get the InlineKeyboardMarkup
                await callback.message.answer("Sorry, I don't have an answer for that.", reply_markup=reply_markup)

        elif data == 'back_to_faq':
            await show_faq_options(callback)
        elif data == "how_is_our_coffee_made":
            await handle_how_is_our_coffee_made_faq_answer(callback)
        elif data == "who_are_we":
            await handle_who_are_we_answer_faq_answer(callback)

        elif data == 'start':
            await start_menu(callback.message)
        elif data == 'buy':
            """This is where the function to display time-slot 
            dashboard buttons to the user.."""
            await callback_handler_buy(callback)
        elif data.startswith("time_slot_"):
            """This is where the function to ask user to confirm
            Order for specified time-slot."""
            await process_selected_time_slot(callback)

        elif data.startswith("confirm_buy"):
            """This is where the actual purchase logic gets called."""
            # Return message to the user, which they can copy, contains; 'time_slot_id', and specified time.
            """"User is prompted to send a message to the admin @handle acc"""
            await booking_specified_time_slot_user_message(callback)
            # """Display a order recap to the user."""
            # await order_recap_customer_message(callback, status=True)  # Either they have payed or failed payment action

        elif data.startswith("admin_manage_booking_time_slot_"):
            await admin_managing_specified_time_slot_booking_choose_true_false(callback)
            print()

        elif data.startswith("admin_managing_specified_time_slot_booking_True_") or ("admin_managing_specified_time_slot_booking_False_"):
            logger.info(f"We made it to 'admin_modify_time_slot_booking_status'")
            await admin_modify_time_slot_booking_status(callback)

        else:
            await handle_unexpected_message(callback.message)

        await callback.answer()

    except Exception as e:
        print(f"Error handling callback query: {e}")
        # Handle the error, perhaps notify the user or log the issue
