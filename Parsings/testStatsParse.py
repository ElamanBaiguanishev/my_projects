import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from parse_lua import parse_lua


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filename):
        self.filename = filename

    def on_modified(self, event):
        if event.src_path.endswith(self.filename):
            self.process_file()

    def process_file(self):
        try:
            parse_lua(self.filename)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found.")


def monitor_file(filename):
    event_handler = FileChangeHandler(filename)
    observer = Observer()
    observer.schedule(event_handler, path='D:/SteamLibrary/steamapps/common/Dawn of War Soulstorm/Profiles/Profile1/')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    filename = 'D:/SteamLibrary/steamapps/common/Dawn of War Soulstorm/Profiles/Profile1/testStats.Lua'  # Укажите имя вашего JSON файла
    monitor_file(filename)
