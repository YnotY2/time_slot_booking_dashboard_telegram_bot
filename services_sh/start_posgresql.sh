#!/bin/bash

start_postgresql() {
    sudo systemctl start postgresql
    echo "PostgreSQL service started successfully."
}

# Call the function to start PostgreSQL
start_postgresql
