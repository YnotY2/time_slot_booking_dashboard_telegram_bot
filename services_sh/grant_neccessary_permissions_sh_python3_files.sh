#!/bin/bash

# Navigate to the services_sh directory
cd ./services_sh || exit

# Give executable permissions to all files
chmod +x *

# Navigate one dir back
cd ..

# Navigate to the services_python3 directory
cd ./services_python || exit

# Give executable permissions to Python files except __init__.py
find . -type f -name '*.py' ! -name '__init__.py' -exec chmod +x {} +
