#!/bin/bash

check_status_postgresql_service() {
    echo "Systemctl status postgresql:"
    sudo systemctl status postgresql
}

# Call the function to check status service PostgreSQL
check_status_postgresql_service
