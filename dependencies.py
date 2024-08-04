
from utils.logger import setup_logger
logger = setup_logger(service_name="Class_DependencyContainer")

# This is used to pass the pool object for database cursor connections to functions.

class DependencyContainer:
    def __init__(self):
        self.pool = None

    def set_pool(self, pool):
        self.pool = pool

    def get_pool(self):
        return self.pool

# Create a global instance of the dependency container
container = DependencyContainer()
