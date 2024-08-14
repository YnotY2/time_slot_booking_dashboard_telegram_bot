# Managing bookings and access for any specified service via telegram
Telegram Bot for any service requiring booking's and user authentication on arrival. Currently I have modified the code to work for a tattoo-shop
as a example.

- **Maximum Booking Horizon:** 46 hours in advance.
- **Minimum Booking Horizon:** 0 hours in advance.
- **Standard Booking Slot** 2 hour long window

**This approach is fully automatic, meaning:**
- When a time slot expires (i.e., its `end_time` is earlier than the current time), it is removed from the `time_slots` table, ensuring it is not displayed to users.
- The population of time slots occurs every hour, ensuring that new time slots are continuously generated, maintaining availability for booking up to 46 hours in advance.

## Features:
-   Main Menu ✅
-   Button Interaction Only ✅
-   FAQ within Menu ✅
-   User booking time-slot dasboard ✅
-   Admin manegement dashboard for all available booking ✅
    - Booking any specified time-slot ☑️
    - Un-booking any specified time-slot ☑️
    - Returns 5 digit PIN when booking time-slot ☑️
    - Unique password cmd for access dashboard via chat message ☑️
        - *Password is set within 'settings.py'* 
-   User 5 digit PIN authentication dasboard ✅
    - authenticating booking on arrival ☑️
    - Accepts or rejects access ☑️
    - Authentication message response based on entered PIN  ☑️
        - *pin is returned to admin after confirming booking* 
    - ```
      user_access_auth_return_data = {
                    'pin_valid': pin_valid,
                    'pin_inside_time_slot': pin_inside_time_slot,
                    'pin_outside_time_slot': pin_outside_time_slot,
                    'start_time': start_time,
                    'end_time': end_time
    
                }
      ```
-   Only available during openings-hours ✅
-   asynchronous  ✅
-   Database ✅
-   Handles unexpected message ✅
    -   *Displays the start_menu command to press*

![Main Time Slot Bot Image](./images/main_time_slot_bot_img_girl.png)

![Access Pin Auth Dashboard](./images/access_pin_auth_dashboard.png)

## Table of Contents

1. [Managing Bookings and Access for Any Specified Service via Telegram](#managing-bookings-and-access-for-any-specified-service-via-telegram)
2. [Features](#features)

4. [Installation](#installation)
   - [Cloning Git Repository](#cloning-git-repository)
   - [Installing requirements](#installing-requirements)
   - [Getting API Key from BotFather](#getting-api-key-from-botfather)
    - [Works out of the box 📦](#works-out-of-the-box-)
        - [Configuration](#configuration)
        - [1. Update Configuration Settings](#1-update-configuration-settings)
        - [2. Update FAQ Data](#2-update-faq-data)
        - [3. Customizing Start Menu [Main-Menu]](#3-customizing-start-menu-main-menu)
        - [4. Modifying Opening Hours](#4-modifying-opening-hours)

5. [Understanding Code Layout](#understanding-code-layout)
   - [Directory Layout](#directory-layout)
   - [Summary](#summary)

6. [Database Schema](#database-schema)
   - [Database Schema Visualized](#database-schema-visualised)
   - [`init-db.spql`](#init-dbspql)
   - [Interacting with the Database Asynchronously Without Blocking](#interacting-with-the-database-asynchronously-without-blocking)
     - [How `DependencyContainer` and `initialize_connection_pool` Work Together](#how-dependencycontainer-and-initialize_connection_pool-work-together)
     - [Imports Used](#imports-used)

   - [Understanding Usage of Tables](#understanding-usage-of-tables)
     - [`time_slots` Table](#time_slots-table)
         - [Functions Utilizing `time_slots` Table](#functions-utilizing-time_slots-table)
            - [populate_time_slots](#1-populate_time_slots)
            - [fetch_all_available_time_slots](#2-fetch_all_available_time_slots)
            - [fetch_time_slot_row_by_id](#3-fetch_time_slot_row_by_id)
            - [fetch_all_time_slots](#4-fetch_all_time_slots)
            - [manage_booking_time_slots](#5-manage_booking_time_slots)
            - [check_user_access_by_access_pin](#6-check_user_access_by_access_pin)

     - [`pins` Table](#pins-table)
        - [Functions Utilizing `pins` Table](#functions-utilizing-pins-table)
            - [fetch_user_entered_access_pin_stored_db](#1-fetch_user_entered_access_pin_stored_db)
            - [insert_or_update_user_entered_access_pin_db](#2-insert_or_update_user_entered_access_pin_db)
            - [delete_user_entered_access_pin_db](#3-delete_user_entered_access_pin_db)

7. [CallbackQuery Handlers](#callbackquery-handlers)
    - **[Start Callback Data Handler](#handle_start_callback)**
    - **[FAQ Callback Data Handlers](#handle_faq_callbacks)**
    - **[Admin Dashboard Callback Data Handlers](#handle_admin_dashboard_callbacks)**
    - **[Booking Order Callback Data Handlers](#handle_booking_order_callback)**
    - **[Access Service Callback Data Handlers](#handle_access_service_callback)**

8. [Advanced Usage: Understanding Code Flow and Customization](#advanced-usage-understanding-code-flow-and-customization)
    - [Review the Entire Documentation](#1-review-the-entire-documentation)
    - [Understand Callback Query Handlers](#2-understand-callback-query-handlers)
    - [Populate Time Slots Logic](#3-populate-time-slots-logic)
    - [Modify Code to Fit Your Needs](#4-modify-code-to-fit-your-needs)
    - [Additional Resources](#5-additional-resources)
    - [Conclusion](#conclusion)
  
<br>
<br>
<br>
<br>

## Installation
### Cloning Git Repository
To clone Git repository using the command line, follow these simple steps:

1. Navigate to the dirctory on you're computer you wish to start coding.
2. Clone this GitHub repo:
```
git clone git@github.com:YnotY2/<public_repo_link>.git
```

<br>

### Installing requirements
To install requirements using the command line, follow these simple steps:

1. Navigate to the dir containing the 'requirements.txt' file.
2. Install the requirements:
```
pip install -r requirements.txt
```

<br>
<br>
<br>
<br>

### Getting API Key from BotFather

To use the Telegram Bot API, you need to obtain an API key from BotFather. Follow these steps to get your API key:

## Steps to Get Your API Key

1. **Start a Chat with BotFather**
   - Open Telegram and search for [BotFather](https://t.me/botfather).
   - Start a chat with BotFather by clicking "Start" or typing `/start`.

2. **Create a New Bot**
   - Type the command `/newbot` and send it.
   - BotFather will ask you to provide a name for your bot. Enter a name (e.g., "MyBot").
   - Next, provide a username for your bot. This username must end in `bot` (e.g., "my_bot").

3. **Receive Your API Key**
   - Once you've provided the name and username, BotFather will create your bot and give you an API key.
   - The API key will be in the format: `123456789:ABCdefGHIjklMNOpqrSTUVwxyZ`.
   - Copy this API key as you'll need it to configure your bot.

4. **Save the API Key**
   - Keep your API key secure and do not share it with others.
   - Use this API key to authenticate requests to the Telegram Bot API.
  
5. **Place the API Key within config/settings.py file**
   - Open the following above mentioned file within you're project directory structure.
   - Then paste you're key in the placement of 'telegram_bot_token' variable value

   This is the 'settings.py' file:
   ```
   import os

   # Database PostgreSQL Credentials
   postgresql_db_name = os.getenv("postgresql_db_name","example_database_name")
   postgresql_db_passwd = os.getenv("postgresql_db_passwd", "example_password")
   postgresql_db_usr = os.getenv("postgresql_db_usr", "example_database_user")
   postgresql_port = os.getenv("postgresql_port", "5432")      # Default port// Change if wanted
   postgresql_host = os.getenv("postgresql_host", "localhost")      # Locally hosted db// Change if wanted
   
   # Telegram Bot API TOKEN:       [unique token to identify the bot and communicate with it.]
   telegram_bot_token = os.getenv("telegram_bot_token", "PASTE_YOUR_API_KEY_HERE")
   
   # Images to send to users within chat:
   start_menu_image_voucher_applied_logo = os.getenv("start_menu_image_logo", "./images/start_menu_image_logo.png")

   # Admin manage time-slot bookings dashboard access password string:
   admin_manage_bookings_dashboard_password = os.getenv("admin_manage_bookings_dashboard_password", "/<youre_complex_password_here>")
   ```

<br>
<br>
<br>
<br>



## Works out of the box 📦

This project is configured to work out of the box with default settings. However, you'll need to customize several configuration files to tailor the application to your needs. Follow the instructions below to modify database credentials, images, FAQ content, and more.

## Configuration

### 1. Modify *'open_specified_amount_hyper_terminal_windows'* Settings

You need to modify the `/home/coding/python3/personal_tools/hyper_terminals_on_startup/run_on_startup/settings.py` file to include your own database credentials, Telegram Bot API token, and other configurations.

####  `./config/settings.py`:

```python
import os

# Database PostgreSQL Credentials
postgresql_db_name = os.getenv("postgresql_db_name", "your_db_name")
postgresql_db_passwd = os.getenv("postgresql_db_passwd", "your_db_password")
postgresql_db_usr = os.getenv("postgresql_db_usr", "your_db_user")
postgresql_port = os.getenv("postgresql_port", "5432")      # Default port // Change if needed
postgresql_host = os.getenv("postgresql_host", "localhost")  # Locally hosted db // Change if needed

# Telegram Bot API TOKEN
telegram_bot_token = os.getenv("telegram_bot_token", "your_bot_token")

# Images to send to users within chat:
start_menu_image_logo = os.getenv("start_menu_image_logo", "./images/start_menu_image_logo.png")
how_is_our_tattoo_made_video = os.getenv("how_is_our_tattoo_made_video", "./videos/how_is_our_tattoo_made.mp4")

# Admin manage time-slot bookings dashboard access password string:
admin_manage_bookings_dashboard_password = os.getenv("admin_manage_bookings_dashboard_password", "your_dashboard_password")
```

<br>
<br>

### 2. Update FAQ Data

Modify the FAQ data and answers in `./config/faq_data.py` and `./config/faq_answers.py` respectively.
Make sure when modifying that the variable holding the value matches in 'faq_data' and 'faq_answers'. For e.g; 'faq_opening_hours' and 'faq_opening_hours'. 
You can change the variable and the value, just make sure they match. As the logic matches both variables to find data to display and answer corresponding question. 
You can also add more FAQ questions and answer only be modifying these files. 

#### `./config/faq_data.py`:

```python
from utils.logger import setup_logger
logger = setup_logger(service_name="faq_data")

# Frequently asked questions
faq_data = {
    "faq_years_of_experience": "How many years of experience?",
    "faq_opening_hours": "Opening hours?",
    "faq_accepted_payment_options": "What payment methods are accepted?",
    "faq_contact_info": "Contact Info?",
    "how_is_our_tattoo_made": "How is your tattoo made?",
}
```

```
from utils.logger import setup_logger
logger = setup_logger(service_name="faq_answers")

# Frequently asked questions matching answers
# The callback_data string argument is the same for answers and data, see 'faq_data.py'
faq_answers = {
    "faq_years_of_experience": (
        "♣️ Years of Experience:\n"
        "\n"
        "With over a decade of experience in the tattoo industry, our talented artists "
        "bring a wealth of knowledge and skill to every design. Their journey began "
        "in the early 2010s, and since then, they've honed their craft through countless "
        "hours of practice and a deep passion for body art. From mastering traditional "
        "styles to exploring contemporary trends, our artists have developed a reputation "
        "for exceptional artistry and precision. Each tattoo is a testament to their "
        "commitment to quality and their dedication to making every client's vision come to life. "
        "Their extensive experience ensures that you receive not only a beautiful tattoo but "
        "also a professional and enjoyable experience."
    ),
    "faq_opening_hours": (
        "🕣 Openings Hours:\n"
         "\n"
         "🎴 Monday:       16:00 - 23:00\n"
         "🎴 Tuesday:      16:00 - 22:00\n"
         "🎴 Wednesday:    16:00 - 0:00\n"
         "🎴 Thursday:     16:00 - 2:00 PM\n"
         "🎴 Friday:       16:00 - 2:00 PM\n"
         "🎴 Saturday:     17:00 - 4:00\n"
         "🎴 Sunday:       17:00 - 4:00\n"
         "\n"
    ),
    "faq_accepted_payment_options": (
        "️ We accept the following payment methods:\n"
        "\n"
        "🎴 Ideal\n"
        "\n"
        "🎴 Paypal\n"
        "\n"
        "🎴 Cash\n"
    ),
    "faq_contact_info": (
        "️📋 Contact Info:\n"
        "\n"
        "📞 PhoneNumber:     (555) 123-4567\n"
        "✉️ Email:              contact@lucytattoo.com\n"
    ),
    "how_is_our_tattoo_made": (
        "\n"
        "Our Coffee Is made with love and care :\n"
        "\n"
    ),

}
```

<br>
<br>

### 3. Customizing Start Menu [Main-Menu]

This document provides instructions for modifying the start menu displayed to users when they initiate a conversation with the bot. You can adjust the welcome message, replace the image, and customize the options available on the start menu.

**Locate the Start Menu Code**

The start menu is configured in the `/home/coding/python3/personal_tools/hyper_terminals_on_startup/run_on_startupser_handlers.py` file. Here is the relevant section of the code:

```python
@user_router.message(Command('start'))
async def start_menu(message: types.Message):
    # Check if message is received between opening hours
    if not check_if_time_within_openings_hours():
        await message.answer("Sorry, 🕣\n"
                             "\n"
                             "The shop is only available between:\n"
                             "8:00 - 23:50 | EU UTC+2. ")
        return

    faq_button = InlineKeyboardButton(text="FAQ", callback_data='faq_menu')
    booking_service_button = InlineKeyboardButton(text="Booking Service", callback_data='booking_service')
    get_access_button = InlineKeyboardButton(text="Access Service", callback_data="access_service")

    # Create an InlineKeyboardMarkup object with a list of rows
    start_keyboard_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [faq_button],         # First row
            [booking_service_button],  # Second row
            [get_access_button],  # Third row
        ]
    )

    photo = FSInputFile(start_menu_image_logo, filename="start_menu_image_logo.png")

    # Send the photo with caption and inline keyboard
    await message.answer_photo(
        photo=photo,
        caption=(
            '\n'
            'Welcome to Lucy Tattoo Shop!\n'
            "We're here to assist you. Please choose from the following options: :\n"
            '\n'
            '🌑 Have any other questions? Click "FAQ" \n'
            '🌑 If you want to book an appointment, click "Booking Service"\n'
            '🌑 To provide booking ID on arrival, click "Access Service" \n'
            '\n'
            'Pricing: \n'
            '350-900€ 💶'
        ),
        reply_markup=start_keyboard_inline
    )

```


 **Locate the Caption Parameter**

In the `./bot/handlers/user_handlers.py` file, find the `await message.answer_photo()` function call. The `caption` parameter contains the text that will be displayed to the user.

Example:
```python
caption=(
   '\n'
   'Welcome to Lucy Tattoo Shop!\n'
   "We're here to assist you. Please choose from the following options: :\n"
   '\n'
   '🌑 Have any other questions? Click "FAQ" \n'
   '🌑 If you want to book an appointment, click "Booking Service"\n'
   '🌑 To provide booking ID on arrival, click "Access Service" \n'
   '\n'
   'Pricing: \n'
   '350-900€ 💶'
)
```

- Edit the caption string to update the welcome message, instructions, or any other text you want to display. You can also change the emoji or pricing information to fit your business.

<br>
<br>

### 4. Modifying Opening Hours

To adjust the opening hours for the bot, you will need to update the `check_if_time_within_openings_hours.py` script. By default, the script is set to check if the current time is between 00:00 (midnight) and 23:59 (one minute before midnight), meaning it is closed only for one minute each day.

 **Adjust the Opening Hours**
Locate and open the `/home/coding/python3/personal_tools/hyper_terminals_on_startup/run_on_startupenings_hours.py` file in your project directory.


Find the function definition `check_if_time_within_openings_hours` and modify the `start_hour`, `start_minute`, `end_hour`, and `end_minute` parameters to set your desired opening hours.

- **`start_hour`**: Set the hour at which the bot opens (24-hour format).
- **`start_minute`**: Set the minute at which the bot opens.
- **`end_hour`**: Set the hour at which the bot closes (24-hour format).
- **`end_minute`**: Set the minute at which the bot closes.

For example, if you want the bot to operate from 8:00 AM to 8:00 PM, update the function call as follows:

```python
check_if_time_within_openings_hours(start_hour=8, start_minute=0, end_hour=20, end_minute=0)
```


## Conclusion
This integration provides a robust system for managing and booking time slots via a Telegram Bot. It includes functionalities for populating the database, fetching available slots, and handling user interactions effectively. Ensure proper handling of errors and resource management to maintain the system's reliability.

