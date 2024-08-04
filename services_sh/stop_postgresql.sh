#!/bin/bash

stop_postgresql() {
    sudo systemctl stop postgresql
    echo "PostgreSQL service stopeed successfully."
}

# Call the function to start PostgreSQL
stop_postgresql
