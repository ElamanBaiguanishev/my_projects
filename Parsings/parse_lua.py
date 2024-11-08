from lupa import LuaRuntime
import win32file
import pywintypes
import pprint


def read_file_with_shared_access(filename):
    # Открываем файл с разделением доступа
    handle = win32file.CreateFile(
        filename,
        win32file.GENERIC_READ,
        win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
        None,
        win32file.OPEN_EXISTING,
        0,
        None
    )

    # Читаем содержимое файла
    try:
        _, data = win32file.ReadFile(handle, 1024*1024)
        return data.decode('utf-8')
    finally:
        handle.Close()


def parse_lua(filename):
    lua = LuaRuntime(unpack_returned_tuples=True)

    lua_code = read_file_with_shared_access(filename)

    lua.execute(lua_code)

    GSGameStats = lua.globals().GSGameStats

    def lua_table_to_dict(lua_table):
        return {k: (lua_table_to_dict(v) if hasattr(v, 'items') else v) for k, v in lua_table.items()}

    game_stats = lua_table_to_dict(GSGameStats)

    teams = {}

    for key, value in game_stats.items():
        if key.startswith('player_'):
            team_id = value['PTeam']
            if team_id not in teams:
                teams[team_id] = []
            teams[team_id].append((key, value))

    ordered_teams = []
    for team_id in sorted(teams.keys()):
        sorted_players = sorted(teams[team_id], key=lambda x: int(x[0].split('_')[1]))
        ordered_teams.append(sorted_players)

    pprint.pprint(ordered_teams)
