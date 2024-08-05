# Time Slots Database and Telegram Bot Integration

## Overview

This project involves managing time slots, aka booking GUI. in a database and providing an interface (GUI) via a Telegram Bot for users to view and book available time slots. The system includes functionality to populate time slots, fetch available slots, and handle user interactions through the bot.

Once a time-slot is booked, it is placed on 'is_booked' = True, and will not be displayed to a user when selecting a new time-slot. Only display available 
time-slots for booking. 

- **Maximum Booking Horizon:** 46 hours in advance.
- **Minimum Booking Horizon:** 2 hours in advance.

**This approach is fully automatic, meaning:**
- When a time slot expires (i.e., its `end_time` is earlier than the current time), it is removed from the `time_slots` table, ensuring it is not displayed to users.
- The population of time slots occurs every 2 hours, ensuring that new time slots are continuously generated, maintaining availability for booking up to 46 hours in advance.

## Database Schema

The `time_slots` table in the database contains the following columns:

- `id`: Unique identifier for each time slot.
- `start_time`: The start time of the time slot.
- `end_time`: The end time of the time slot.
- `is_booked`: A boolean flag indicating whether the slot is booked.

'init-db.spql'
```
-- Create the time_slots table
CREATE TABLE time_slots (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    is_booked BOOLEAN DEFAULT FALSE,
    CONSTRAINT unique_time_slot UNIQUE (start_time, end_time)
);

```

## Logic of Time-Slots
### Time Slot Duration

- Each time slot is 2 hours long.

### Slot Population and Management

- **Population Schedule:**
  - A background task runs every 2 hours to populate the `time_slots` table with new time slots. This ensures that the table always has slots available for the next 46 hours.

   - This task is ran within 'main.py'
  - Using the following functions: *'periodic_task' and 'populate_time_slots'*. :
  ```
    database_task_1 = asyncio.create_task(periodic_task(7200, populate_time_slots))
  ```
  - *The above task we are running is 'populate_time_slots'*
  - *The 'periodic_task' could in theory schedgule any async task*

- **Time Slot Records:**
  - The population task does not modify existing records. Specifically:
    - **Existing Slots:** Time slots that are already in the table will not be altered.
    - **`is_booked` Status:** The `is_booked` status of time slots is preserved. The task does not change the status from `TRUE` to `FALSE` or vice versa.
    - **Expired Slots:** Time slots that have ended (i.e., their end time is before the current time) are removed from the table.

- **Populate Time Slots Function (`populate_time_slots`):**
  - This function populates the database with time slots for the upcoming 46 hours, ensuring that it doesn't delete or modify existing slots that are still within their booking period.


## Functions

### 1. `populate_time_slots`

**Description:**

Populates the `time_slots` table with time slots for the next 46 hours. It ensures that booked slots are not removed unless their end time has passed.

**Logic:**

1. **Setup Timezone and Time Range:**
   - Use `Europe/Paris` timezone.
   - Define the current time and the end time 46 hours from now.
   - Set a 2-hour interval for time slots.

2. **Align Start Time:**
   - Adjust the current time to the nearest previous hour.

3. **Database Operations:**
   - Delete time slots that have ended.
   - Insert new time slots if they do not already exist.

4. **Error Handling:**
   - Log errors if they occur during database operations.

5. **Resource Management:**
   - Ensure the database connection is properly returned to the pool.

### Code Explanation
**2** main parts of *logic* to this function!

1. **Purpose:**
   - The purpose of this code is to delete entries from the `time_slots` table where the `end_time` of the time slot is earlier than the current time. This ensures that expired time slots are removed from the table and are not shown to users.

```
"""Delete old table rows, where time-slot has ended."""
delete_old_slots_query = """
    DELETE FROM time_slots 
    WHERE end_time < %s
"""
await cursor.execute(delete_old_slots_query, (now,))

```

2. **SQL Query:**
   - The SQL query defined by the `delete_old_slots_query` string:
     ```sql
     DELETE FROM time_slots 
     WHERE end_time < %s
     ```
     This query deletes rows from the `time_slots` table where the `end_time` column has a value less than the specified timestamp (represented by `%s`).

3. **Parameter Substitution:**
   - The `%s` placeholder in the SQL query is used for parameter substitution. The actual value to replace `%s` is provided in the tuple `(now,)`.

4. **Executing the Query:**
   - The `await cursor.execute(delete_old_slots_query, (now,))` line executes the SQL query asynchronously. Here, `cursor` is the database cursor object used to execute database commands. The `now` variable holds the current timestamp and is passed as the parameter to replace `%s` in the SQL query.

5. **Result:**
   - The result of this operation is that any time slot entries in the `time_slots` table with an `end_time` earlier than the current time (`now`) will be deleted. This helps in keeping the table up-to-date and relevant by removing outdated time slots.






### 2. `fetch_all_available_time_slots`

**Description:**

Fetches all available time slots that are between 2 hours and 46 hours from now, ordered in reverse chronological order.

**Logic:**

1. **Setup Time Window:**
   - Define the current time and the boundaries for fetching available slots (2 to 46 hours from now).

2. **Database Query:**
   - Retrieve slots where `is_booked` is `FALSE` and within the defined time window.
   - Order results by `start_time` in descending order.

3. **Error Handling:**
   - Log errors if they occur during database operations.

4. **Resource Management:**
   - Ensure the database connection is properly returned to the pool.

### 3. `fetch_time_slot_row_by_id`

**Description:**

Fetches a specific time slot by its ID if it is not booked.

**Logic:**

1. **Database Query:**
   - Retrieve the time slot with the given ID where `is_booked` is `FALSE`.

2. **Error Handling:**
   - Log errors if they occur during database operations.

3. **Resource Management:**
   - Ensure the cursor and connection are returned to the pool.

### 4. `callback_handler_buy`

**Description:**

Handles callback queries to display time slots and additional buttons when the 'buy' button is pressed.

**Logic:**

1. **Create Time Slot Buttons:**
   - Fetch available time slots and create inline keyboard buttons for each slot.

2. **Handle No Slots Available:**
   - If no slots are available, notify the user and provide options to return to the main menu or view FAQs.

3. **Display Time Slots:**
   - Show time slots with their respective buttons and additional navigation options.
  
### `create_time_slot_buttons`

**Description:**

This function generates inline keyboard buttons for Telegram messages based on the available time slots provided. Each button represents a time slot that users can select.

**Parameters:**

- `available_time_slots`: A list of dictionaries where each dictionary represents a time slot with the following keys:
  - `id`: Unique identifier of the time slot.
  - `start_time`: Start time of the time slot.
  - `end_time`: End time of the time slot.

**Logic:**

1. **Check for Empty Slots:**
   - If the `available_time_slots` list is empty, the function returns `None`. This indicates that no time slots are available to display.

2. **Initialize Keyboard Layout:**
   - Create an empty list called `keyboard` to hold the rows of buttons.

3. **Generate Buttons:**
   - Iterate over the `available_time_slots` list using a loop.
   - For each slot, format the `start_time` and `end_time` to a string that shows the day and time. The format used is "day HH:MM" for the start time and "HH:MM" for the end time.
   - Create a button for each time slot using `InlineKeyboardButton`. The button's text displays the formatted time range, and its `callback_data` contains the slot's ID prefixed with "time_slot_".

4. **Arrange Buttons in Rows:**
   - Buttons are arranged in rows. If the index `i` is even, start a new row by appending a new list containing the button to `keyboard`.
   - If the index `i` is odd, add the button to the last row in `keyboard`.

5. **Return the Keyboard Layout:**
   - Wrap the `keyboard` list in an `InlineKeyboardMarkup` object, which is returned. This object represents the layout of inline buttons that will be sent to the Telegram chat.

**Example Usage:**
If you have two available time slots:
- Slot 1: Start time "2024-08-06 10:00", End time "2024-08-06 12:00"
- Slot 2: Start time "2024-08-06 14:00", End time "2024-08-06 16:00"

The `create_time_slot_buttons` function will produce a keyboard layout with two buttons, each formatted with their respective time ranges. These buttons will be displayed in a Telegram message, allowing users to select a time slot.

**Returns:**

An `InlineKeyboardMarkup` object that can be used to send an inline keyboard to a Telegram chat. If no time slots are available, the function returns `None`.


### 5. `process_selected_time_slot`

**Description:**

Processes the selection of a time slot by the user.

**Logic:**

1. **Extract Callback Data:**
   - Parse the callback data to get the time slot ID.

2. **Fetch Time Slot Details:**
   - Retrieve the details of the selected time slot.

3. **Display Confirmation:**
   - Show the user the start and end times of the selected slot and provide options to confirm the booking or return to the main menu.

## Conclusion

This integration provides a robust system for managing and booking time slots via a Telegram Bot. It includes functionalities for populating the database, fetching available slots, and handling user interactions effectively. Ensure proper handling of errors and resource management to maintain the system's reliability.

