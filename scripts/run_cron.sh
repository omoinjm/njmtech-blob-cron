#!/bin/bash
set -e

# Ensure we have a standard PATH for the cron environment
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# This script is intended to be run by a cron job.
# It ensures that the Python application is executed in the correct environment.

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR" || exit

echo "[$(date)] CRON START: Running NJMTech Blob Cron Job"

# Execute the main python script using python3.
python3 main.py

echo "[$(date)] CRON FINISHED: NJMTech Blob Cron Job"
echo "----------------------------------------"
