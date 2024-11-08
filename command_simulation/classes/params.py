# import random
#
# from tools.tools_dirs import get_serial_tome
#
#
# class Bytes:
#     def __init__(self):
#         self.a = random.randint(10, 60)
#         self.b = random.randint(200, 999)
#         self.c = random.randint(100, 999)
#         self.d = random.randint(500, 999)
#
#     def __str__(self):
#         return f"{self.a} {self.b} {self.c} {self.d}"
#
#
# class Params:
#     def __init__(self, main_path):
#         self.memory = 10000
#         self.serial_tome = get_serial_tome()
#         self.main_path = main_path
#         self.bytes_dir = Bytes()
