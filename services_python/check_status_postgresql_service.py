import subprocess
import re
from utils.colors import Colors
from utils.logger import setup_logger

# Set up logger with service name
service_name = "check_status_postgresql_service"
logger = setup_logger(service_name)


def check_status_postgresql_service():
    try:
        # Construct the command to execute the shell script
        script_path = "./services_sh/check_status_postgresql_service.sh"  # Adjust the path as necessary
        logger.info(f"{Colors.CYAN}Executing check_status_postgresql_service.sh script{Colors.END}")

        # Execute the shell script using subprocess and capture the output
        process = subprocess.Popen(script_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0 or 3:
            logger.info(f"{Colors.GREEN}Status check on PostgreSQL service completed successfully [output captured].{Colors.END}")

            # Decode the stdout from bytes to string
            output = stdout.decode('utf-8')
            logger.info(f"{Colors.CYAN}Script output{Colors.END}{Colors.BLUE}: {output}{Colors.END}")
            print("")

            # Parse the output with a regular expression
            match = re.search(r'Active:\s+(\w+)', output)
            if match:
                status = match.group(1)
                logger.info(f"{Colors.CYAN}PostgreSQL service status captured:{Colors.GREEN}{Colors.MAGENTA} {status}{Colors.END}")
                if status == "active":
                    logger.info(f"{Colors.GREEN}The PostgreSQL service is active.{Colors.END}")
                    return True

                else:
                    logger.info(f"{Colors.CYAN}The PostgreSQL service is not active. Current status: {status}{Colors.END}")
                    return False
            else:
                logger.warning(f"{Colors.RED}No matching pattern found in script output.{Colors.END}")
                return False

        else:
            logger.error(f"{Colors.RED}Error in executing script: {stderr.decode('utf-8')}{Colors.END}")
            print(process.returncode)
            return False


    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(f"{Colors.RED}Error: Executing check_status_postgresql_service.sh {Colors.END}")
        return False

    # Print a blank line to the terminal
    print("")


if __name__ == "__main__":
    check_status_postgresql_service()
