# CodexKeep/scripts/error_handling.py

import sys
import time
import traceback

ERROR_LOG_FILE = "error_log.txt"
ERROR_LOG = []


def log_error(error_message, is_critical=False):
    """
    Log errors to file and in-memory log.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] {'CRITICAL' if is_critical else 'ERROR'}: {error_message}"
    )
    ERROR_LOG.append(log_entry)
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry + "\n")
    print(log_entry)


def log_batch_error(batch_number, message):
    """

    Log an error that occurred during batch processing.

    """

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] BATCH {batch_number} ERROR: {message}"

    ERROR_LOG.append(log_entry)

    print(log_entry)


def handle_critical_error(error_message, exit_on_failure=True):
    """
    Handle critical errors and decide whether to exit.
    """
    log_error(error_message, is_critical=True)
    if exit_on_failure:
        sys.exit(1)
