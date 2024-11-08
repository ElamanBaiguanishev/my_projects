import win32gui


def find_window_partial(title):
    def enum_windows_callback(hwnd, results):
        if title in win32gui.GetWindowText(hwnd):
            results.append(hwnd)

    results = []
    win32gui.EnumWindows(enum_windows_callback, results)
    if results:
        return results[0]
    raise Exception(f"Window containing title '{title}' not found!")


hwnd = find_window_partial('Dawn of War: Soulstorm')

print(f"Target window HWND: {hwnd}")
# 395710

