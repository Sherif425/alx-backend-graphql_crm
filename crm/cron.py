import datetime
import os

def log_crm_heartbeat():
    """
    Logs a heartbeat message to a file to confirm the CRM application's health.
    This function is intended to be run as a cron job.
    """
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    try:
        # Open the file in append mode to avoid overwriting existing logs
        with open(log_file_path, 'a') as f:
            f.write(message)
    except IOError as e:
        # Log an error if the file cannot be written
        print(f"Error writing to heartbeat log file: {e}")