from ctypes import *
from ctypes.wintypes import *
import win32ui, win32process, win32gui

PROCESS_ALL_ACCESS = 0x1F0FFF

HWND = win32gui.FindWindowEx(None, None, None, 'Dawn of War: Soulstorm')
pid = win32process.GetWindowThreadProcessId(HWND)[1]
OpenProcess = windll.kernel32.OpenProcess  # (PROCESS_ALL_ACCESS,False,pid)
ReadProcessMemory = windll.kernel32.ReadProcessMemory

address = 0x0096F7CC
buffer = create_string_buffer(4)
bufferSize = (sizeof(buffer))
bytesRead = c_ulong(0)

print('HWND: ', HWND)
print('pid: ', pid)
print('buffer: ', buffer)
print('bufferSize: ', bufferSize)

processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

if ReadProcessMemory(processHandle, address, buffer, bufferSize, byref(bytesRead)):
    print("Success:", buffer)
else:
    print("Failed.")

