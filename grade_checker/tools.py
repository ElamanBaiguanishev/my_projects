import logging
import os
from datetime import datetime

group_en_to_ru = {
    "at": "АТ",
    "gv": "ГВ",
    "im": "ИМ",
    "ip": "ИП",
    "lt": "ЛТ",
    "le": "ЛЭ",
    "ng": "НГ",
    "od": "ОД",
    "pv": "ПВ",
    "pt": "ПТ",
    "rs": "РС",
    "sp": "СП",
    "se": "СЭ",
    "tb": "ТБ",
    "td": "ТД",
    "tl": "ТЛ",
    "tm": "ТМ",
    "tr": "ТР",
    "eb": "ЭБ",
    "bd": "БД"
}


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


def check_db(_folder_path):
    checks = {"Access": False, "Errors": []}
    if os.access(_folder_path, os.R_OK) and os.access(_folder_path, os.X_OK):
        checks["Access"] = True
    else:
        checks["Access"] = False
    for root, directories, files in os.walk(_folder_path):
        if not directories:
            if 'Студенты.xlsx' not in files or 'Предметы.xlsx' not in files:
                checks["Errors"].append(root)
    return checks


def check_access(_folder_path):
    checks = {"Access": False, "Errors": []}
    if os.access(_folder_path, os.R_OK) and os.access(_folder_path, os.X_OK):
        checks["Access"] = True
    else:
        checks["Access"] = False
    return checks
