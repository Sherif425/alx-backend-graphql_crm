#!/bin/bash

# A shell script to clean up inactive customers in a Django application.

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Ensure the virtual environment's Python is used.
# Assumes the virtual environment is in the project's root directory.
VENV_PYTHON="${PROJECT_DIR}/venv/bin/python"

# Verify the virtual environment python exists.
if [ ! -f "$VENV_PYTHON" ]; then
    echo "$(date): Error: Virtual environment Python not found at $VENV_PYTHON. Cannot run cleanup." >> "$LOG_FILE"
    exit 1
fi

# Use Django's shell to execute the cleanup logic.
# The command finds customers with no orders in the last year and deletes them.
# It then prints the number of deleted customers.
CLEANUP_COMMAND="
import datetime
from django.utils import timezone
from crm.models import Customer, Order
one_year_ago = timezone.now() - datetime.timedelta(days=365)
inactive_customers_ids = Customer.objects.exclude(order__date_placed__gte=one_year_ago).values_list('id', flat=True)
deleted_count, _ = Customer.objects.filter(id__in=inactive_customers_ids).delete()
print(f'{{deleted_count}} customers deleted.')
"

# Execute the Django command and log the output.
# The `set -o pipefail` ensures the script exits with a non-zero status if any part of the pipe fails.
set -o pipefail
RESULT=$(${VENV_PYTHON} "${PROJECT_DIR}/manage.py" shell -c "${CLEANUP_COMMAND}" | tee /dev/fd/4 4>&1 >/dev/null)
EXIT_STATUS=$?

if [ $EXIT_STATUS -ne 0 ]; then
    echo "$(date): ERROR: Cleanup script failed with exit status ${EXIT_STATUS}. Output: ${RESULT}" >> "$LOG_FILE"
    exit 1
fi

# Log the timestamp and result to the log file
echo "$(date): Cleanup successful. Result: ${RESULT}" >> "$LOG_FILE"

echo "Cleanup script finished. Check log file at $LOG_FILE for details."
