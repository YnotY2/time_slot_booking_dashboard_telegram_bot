from services_python.grant_neccessary_permissions_sh_python3_files import grant_neccessary_permissions_sh_python3_files
from utils.colors import Colors
from utils.logger import setup_logger

# Setup logger with service name
service_name = "grant_permissions"
logger = setup_logger(service_name)

def grant_permissions():
    logger.info(f"{Colors.CYAN}Attempting to grant permissions to needed files, for code to run correctly{Colors.END}")
    try:
        grant_neccessary_permissions_sh_python3_files()

    except Exception as e:
        logger.info(f"{Colors.RED}Error setting up needed file permissions; {e} {Colors.END}")

if __name__ == "__main__":
    grant_permissions()