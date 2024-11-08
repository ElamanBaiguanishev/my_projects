import win32gui
import win32process
import win32con
from ctypes import windll, create_unicode_buffer, wintypes


def find_session_id():
    hwnd = win32gui.FindWindow(None, "Dawn of War: Soulstorm")
    if not hwnd:
        return

    print(hwnd)

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    print(pid)

    h_process = windll.kernel32.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
    if not h_process:
        return

    print(h_process)

    buffer_size = 100000
    buffer = create_unicode_buffer(buffer_size)
    ptr1_count = 0

    while ptr1_count < 0x7FFE0000:
        bytes_read = wintypes.SIZE()

        if not windll.kernel32.ReadProcessMemory(h_process, ptr1_count, buffer, buffer_size, bytes_read):
            # print("kek")
            last_error = windll.kernel32.GetLastError()
            if last_error != 299:
                print("Could not read process memory", ptr1_count, last_error)
            continue

        print("lol")

        for i in range(100, bytes_read.value - 44):

            print(session_header)
            match = True
            for j in range(len(session_header)):
                if buffer[i + j] != session_header[j]:
                    match = False
                    break

            if not match:
                continue

            session_id_str = buffer.raw[i:i + 44].decode("utf-8")[10:44]
            if not session_id_str.endswith("&ack"):
                continue

            session_id_str = session_id_str[:30]

            return session_id_str

        ptr1_count += 100000

    windll.kernel32.CloseHandle(h_process)


session_header = b'\x00' * 44

session_id = find_session_id()
if session_id:
    print("Session ID:", session_id)
else:
    print("Session ID not found.")
