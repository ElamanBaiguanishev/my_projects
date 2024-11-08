import logging
import os


def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, exc_traceback))


def create_log_file():
    log_filename = "logs/error_log.txt"
    logging.basicConfig(filename=log_filename,
                        level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='\n%Y-%m-%d %H:%M:%S')
    return log_filename
