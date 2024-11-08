import os


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
