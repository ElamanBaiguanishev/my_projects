# from classes.cd import Cd
# from classes.dir import Dir
# from classes.params import Params
#
#
# class Main:
#     def __init__(self, main_path):
#         self.params = Params(main_path)
#
#     def create(self):
#         header = f"{self.params.main_path}>"
#
#         dir_instance = Dir(self.params.main_path)
#         cd_instance = Cd(self.params.main_path, "Новая папка")
#         self.params.main_path = cd_instance.get_updated_path()
#
#         result = header + dir_instance.create()
#         result += cd_instance.create_folder()
#
#         dir_instance = Dir(self.params.main_path, folders=["Абоба"])
#         result += dir_instance.create()
#
#         return result
