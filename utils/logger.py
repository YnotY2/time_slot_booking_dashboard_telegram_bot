import logging

def setup_logger(service_name):
    # Create a custom formatter for terminal output
    terminal_formatter = logging.Formatter('%(asctime)s - %(levelname)s - ' + service_name + ' - %(message)s')

    # Create a custom formatter for file output
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Configure logging
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate log messages
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(terminal_formatter)
        logger.addHandler(console_handler)

    return logger
if __name__ == "__main__":
    setup_logger()
