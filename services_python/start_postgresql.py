import subprocess
from utils.colors import Colors
from utils.logger import setup_logger

# Set up logger with service name
service_name = "start_postgresql"
logger = setup_logger(service_name)


def start_postgresql():
    try:
        # Construct the command to execute the shell script
        # The path has a "." to indicate the start dir in this case main.py is located.
        script_path = "./services_sh/start_posgresql.sh"  # Adjust the path as necessary
        command = [script_path]

        logger.info(f"{Colors.CYAN}Executing start_postgresql.sh script{Colors.END}")

        # Execute the shell script using subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            logger.info(f"{Colors.GREEN}PostgreSQL service started successfully.{Colors.END}")
        else:
            logger.error(f"Error: {stderr.decode('utf-8')}")

    except Exception as e:
        logger.error(f"Error: {e}")

    # Print a blank line to the terminal
    print("")


if __name__ == "__main__":
    start_postgresql()

