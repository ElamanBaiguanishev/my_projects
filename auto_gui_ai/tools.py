import logging
import os
from datetime import datetime


def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, exc_traceback))


def create_log_file():
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"{log_folder}/error_log_{current_date}.txt"

    logging.basicConfig(filename=log_filename,
                        level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='\n%Y-%m-%d %H:%M:%S')

    return log_filename
