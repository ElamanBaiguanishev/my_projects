import ctypes
import pyautogui

# def get_layout():
#     u = ctypes.windll.LoadLibrary("user32.dll")
#     pf = getattr(u, "GetKeyboardLayout")
#     if hex(pf(0)) == '0x4190419':
#         return 'ru'
#     if hex(pf(0)) == '0x4090409':
#         return 'en'

# print(pyautogui.position())


# for i in range(100):
#     print(f"https://t.me/user{i}")

list1 = [1, 2, 3]
list2 = [2, 3, 4, 5]

list1.extend(list2)
print(set(list1))
