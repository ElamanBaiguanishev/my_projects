import ctypes
from ctypes import wintypes
import win32process
import win32gui

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
PROCESS_ALL_ACCESS = (PROCESS_QUERY_INFORMATION | PROCESS_VM_READ)
BUFFER_SIZE = 100000

# Define the session header for matching
sessionHeader = bytes([0x73, 0x65, 0x73, 0x73, 0x69, 0x6F, 0x6E, 0x49, 0x44, 0x3D])


def find_session_id():
    hwnd = win32gui.FindWindow(None, 'Dawn of War: Soulstorm')
    if not hwnd:
        print("Window not found.")
        return

    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not process_handle:
        print("Could not open process.")
        return

    buffer = ctypes.create_string_buffer(BUFFER_SIZE)
    bytesRead = ctypes.c_size_t(0)
    ptr1Count = 0x00000000

    while ptr1Count < 0x7FFE0000:
        if ctypes.windll.kernel32.ReadProcessMemory(process_handle, ctypes.c_void_p(ptr1Count), buffer, BUFFER_SIZE,
                                                    ctypes.byref(bytesRead)):
            for i in range(100, bytesRead.value - len(sessionHeader)):
                if buffer[i:i + len(sessionHeader)] == sessionHeader:
                    session_id_str = buffer[i:i + 44].decode('utf-8', errors='ignore')
                    session_id_str = session_id_str[-34:]

                    if session_id_str.endswith("&ack"):
                        session_id_str = session_id_str[:30]
                        print("Session ID:", session_id_str)
                        return
        else:
            if ctypes.windll.kernel32.GetLastError() != 299:
                print(
                    f"Could not read process memory at address {hex(ptr1Count)}. Error: {ctypes.windll.kernel32.GetLastError()}")

        ptr1Count += BUFFER_SIZE


find_session_id()
