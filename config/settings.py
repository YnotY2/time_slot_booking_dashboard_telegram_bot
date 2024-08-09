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