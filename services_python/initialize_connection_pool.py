import aiopg
import asyncio
from utils.colors import Colors
from utils.logger import setup_logger
from config.settings import postgresql_db_name, postgresql_db_passwd, postgresql_db_usr, postgresql_port, \
    postgresql_host

# Set up logger with service name
service_name = "initialize_connection_pool"
logger = setup_logger(service_name)


# In async we need to return also the pool of cursor connections.
async def initialize_connection_pool():
    dsn = f"dbname={postgresql_db_name} user={postgresql_db_usr} password={postgresql_db_passwd} host={postgresql_host} port={postgresql_port}"

    logger.info(f"{Colors.CYAN}Attempting to connect to the following database:{Colors.END}")
    logger.info(f"{Colors.BLUE}database:{Colors.END}{Colors.MAGENTA}        {postgresql_db_name}         {Colors.END}")
    logger.info(f"{Colors.BLUE}user:{Colors.END}{Colors.MAGENTA}            {postgresql_db_usr}         {Colors.END}")
    logger.info(f"{Colors.BLUE}password:{Colors.END}{Colors.MAGENTA}        {postgresql_db_passwd}         {Colors.END}")
    logger.info(f"{Colors.BLUE}host:{Colors.END}{Colors.MAGENTA}            {postgresql_host}         {Colors.END}")
    logger.info(f"{Colors.BLUE}port:{Colors.END}{Colors.MAGENTA}            {postgresql_port}         {Colors.END}")

    try:
        # Create an async connection pool
        pool = await aiopg.create_pool(dsn)
        logger.info(f"{Colors.GREEN}Successfully created the connection pool.{Colors.END}")
        return pool

    except Exception as e:
        logger.error(f"{Colors.RED}Error creating connection pool: {e}.{Colors.END}")
        return None

if __name__ == "__main__":
    asyncio.run(initialize_connection_pool())
