import random
import time

from tools.tools_dirs import get_serial_tome


class Bytes:
    def __init__(self):
        self.a = random.randint(10, 60)
        self.b = random.randint(200, 999)
        self.c = random.randint(100, 999)
        self.d = random.randint(500, 999)

    def __str__(self):
        return f"{self.a} {self.b} {self.c} {self.d}"


main_path = "C:\\Users\\Elaman"
serial_tome = get_serial_tome()
bytes_disk = Bytes()


def dir_folder(folders_dict, files_dict=None):
    header = f" Том в устройстве {main_path[0]} не имеет метки.\n" + f" Серийный номер тома: {serial_tome}\n" + "\n" + f" Содержимое папки {main_path}\n" + "\n"

    folders_str = f"{time.strftime(f'%d.%m.%Y %H:%M')}    <DIR>          .\n" + f"{time.strftime(f'%d.%m.%Y %H:%M')}    <DIR>          .."

    for folder, current_time in folders_dict.items():
        if current_time is None:
            folders_str = folders_str + "\n" + f"{time.strftime(f'%d.%m.%Y %H:%M')}    <DIR>          {folder}"
        else:
            folders_str = folders_str + "\n" + f"{current_time}    <DIR>          {folder}"
    max_space_1 = 15

    files_str = ""
    end_files = ""

    if not files_dict is None:
        files_size = 0

        for file, size in files_dict.items():
            max_space = 18
            len_size = size.__len__()
            space = max_space - len_size
            files_size = files_size + int(size.replace(' ', ''))
            files_str = files_str + "\n" + f"{time.strftime(f'%d.%m.%Y %H:%M')}{' ' * space}{size} " + file

        count_files = files_dict.__len__()
        space_2 = max_space_1 - f"{count_files}".__len__()
        end_files = "\n" + " " * space_2 + str(count_files) + " файлов  " + '{:,}'.format(files_size).replace(',',
                                                                                                              ' ') + " байт"

    count_folders = folders_dict.__len__() + 2
    space_1 = max_space_1 - f"{count_folders}".__len__()
    end_folders = "\n" + " " * space_1 + str(count_folders) + " папок  " + bytes_disk.__str__() + " байт свободно"

    end = end_files + end_folders

    return "dir\n" + header + folders_str + files_str + end + f"\n\n{main_path}>"


def mkdir_folder(folder):
    header = "mkdir " + folder
    return header + "\n\n" + main_path + ">"


res_h = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
         '18', '19', '20', '21', '22', '23']
res_m = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
         '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
         '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53',
         '54', '55', '56', '57', '58', '59']
months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
          "декабря"]


def cd_folder(folder):
    global main_path
    header = "cd " + folder
    main_path = main_path + "\\" + folder
    return header + "\n\n" + main_path + ">"


def get_min(m: int):
    if m > 60:
        return res_m[m % 60]
    else:
        return res_m[m]


def cmd_c():
    m = int(time.strftime("%m"))
    dict_ = {
        "3D Objects": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Contacts": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Desktop": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Documents": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Downloads": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Favorites": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Links": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Music": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "OneDrive": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Pictures": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Saved Games": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Searches": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
        "Videos": time.strftime(f'%d.%m.%Y %H:{get_min(m - random.randint(1, 3))}'),
    }
    return dict_


if __name__ == '__main__':
    result = f"{main_path}>"
    disk_c = cmd_c()

    result += dir_folder(files_dict={"text.txt": "1", "1.mp3": "2 440 968"},
                         folders_dict=disk_c)

    result += mkdir_folder(folder="AAAA")
    disk_c["AAAA"] = None

    result += dir_folder(
        folders_dict=disk_c)

    print(result)
