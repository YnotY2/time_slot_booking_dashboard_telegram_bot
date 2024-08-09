import os

# Database PostgreSQL Credentials
postgresql_db_name = os.getenv("postgresql_db_name","time_slot_telegram_bot_db")
postgresql_db_passwd = os.getenv("postgresql_db_passwd", "083yhbfjlabskhf")
postgresql_db_usr = os.getenv("postgresql_db_usr", "time_slot_telegram_bot_user")
postgresql_port = os.getenv("postgresql_port", "5432")      # Default port// Change if wanted
postgresql_host = os.getenv("postgresql_host", "localhost")      # Locally hosted db// Change if wanted

# Telegram Bot API TOKEN:       [unique token to identify the bot and communicate with it.]
telegram_bot_token = os.getenv("telegram_bot_token", "7191045594:AAFP_I6oZ5MCUuDq88T_KNJItY5npjH2k3A")

# Images to send to users within chat:
start_menu_image_logo = os.getenv("start_menu_image_logo", "./images/start_menu_image_logo.png")
how_is_our_tattoo_made_video = os.getenv("how_is_our_tattoo_made_video", "./videos/how_is_our_tattoo_made.mp4")

# Admin manage time-slot bookings dashboard access password string:
admin_manage_bookings_dashboard_password = os.getenv("admin_manage_bookings_dashboard_password", "/{]BbLrvEE[W@@l2OdwZ-Bylb@8bwmdvYMj")