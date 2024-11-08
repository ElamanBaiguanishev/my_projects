# from classes.params import Params
#
#
# class Cd(Params):
#     def __init__(self, main_path, folder=None):
#         super().__init__(main_path)
#         if folder is None:
#             folder = "default"
#         self.folder = folder
#
#     def create_folder(self):
#         header = "cd " + self.folder
#         self.main_path = self.main_path + "\\" + self.folder
#         return header + "\n\n" + self.main_path + ">"
#
#     def get_updated_path(self):
#         return self.main_path + "\\" + self.folder
