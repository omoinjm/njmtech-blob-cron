#!/bin/bash

# This script is intended to be run by a cron job.
# It ensures that the Python application is executed in the correct environment.

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navigate to the project root directory (one level up from the script's directory)
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR" || exit

echo "Running NJMTech Blob Cron Job at $(date)"

# Activate the virtual environment if using poetry
# and execute the main python script.
# The output will be logged to wherever the cron job's output is redirected.
poetry run python main.py

echo "NJMTech Blob Cron Job finished at $(date)"
echo "----------------------------------------"
