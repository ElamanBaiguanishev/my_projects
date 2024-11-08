# import time
#
# from classes.params import Params
#
#
# class Dir:
#     def __init__(self, main_path, params=Params(), folders=None,
#                  files=None):
#         self.params = Params()
#         if files is None:
#             files = {"text.txt": "1", "1.mp3": "2 440 968"}
#         if folders is None:
#             folders = ["Новая папка", "Documents", "Musics"]
#         self.folders = folders
#         self.files = files
#
#     def create(self):
#         header = f" Том в устройстве {self.params.main_path[0]} не имеет метки.\n" + f" Серийный номер тома: {self.serial_tome}\n" + "\n" + f" Содержимое папки {self.main_path}\n" + "\n"
#
#         folders = f"{time.strftime(f'%d.%m.%Y %H:%M')}    <DIR>          .\n" + f"{time.strftime(f'%d.%m.%Y %H:%M')}    <DIR>          .."
#
#         for folder in self.folders:
#             folders = folders + "\n" + f"{time.strftime(f'%d.%m.%Y %H:%M')}    <DIR>          {folder}"
#
#         files = ""
#
#         files_size = 0
#
#         for file, size in self.files.items():
#             max_space = 18
#             len_size = size.__len__()
#             space = max_space - len_size
#             files_size = files_size + int(size.replace(' ', ''))
#             files = files + "\n" + f"{time.strftime(f'%d.%m.%Y %H:%M')}{' ' * space}{size} " + file
#
#         max_space_1 = 15
#         count_folders = self.folders.__len__() + 2
#         count_files = self.files.__len__()
#         space_1 = max_space_1 - f"{count_folders}".__len__()
#         space_2 = max_space_1 - f"{count_files}".__len__()
#         result = '{:,}'.format(files_size).replace(',', ' ')
#
#         end = "\n" + " " * space_2 + str(count_files) + " файлов  " + result + " байт" + \
#               "\n" + " " * space_1 + str(count_folders) + " папок  " + self.bytes_dir.__str__() + " байт свободно"
#
#         return "dir\n" + header + folders + files + end + f"\n\n{self.main_path}>"
