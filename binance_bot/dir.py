import json
import random
import time
import locale

locale.setlocale(locale.LC_TIME, "ru_RU")

with open('D://bot_ct//data_ct.json', encoding='utf-8') as file:
    file_content = file.read()

data_ct = json.loads(file_content)

second_name = data_ct["f"]
first_name = data_ct["i"]
adapter = data_ct["adapter"]


def get_mac_address() -> str:
    mac_address = '-'.join([hex(random.randint(0, 255))[2:].upper() for _ in range(6)])
    if len(mac_address) == 17:
        return mac_address
    else:
        return get_mac_address()


def get_ip6() -> str:
    ip6 = "fe80::" + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + ":" \
          + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + ":" \
          + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + ":" \
          + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + "%" + str(random.randint(6, 12))
    if len(ip6) in (27, 28):
        return ip6
    else:
        return get_ip6()


def get_DUID() -> str:
    DUID = "00-01-00-01-" + '-'.join([hex(random.randint(0, 255))[2:].upper() for _ in range(10)])
    if len(DUID) == 41:
        return DUID
    else:
        return get_DUID()


def get_serial_tome() -> str:
    serial_tome = hex(random.randint(0, 255))[2:].upper() \
                  + hex(random.randint(0, 255))[2:].upper() \
                  + "-" + hex(random.randint(0, 255))[2:].upper() \
                  + hex(random.randint(0, 255))[2:].upper()
    if len(serial_tome) == 9:
        return serial_tome
    else:
        return get_serial_tome()


res_h = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
         '18', '19', '20', '21', '22', '23']
res_m = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
         '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
         '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53',
         '54', '55', '56', '57', '58', '59']
months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
          "декабря"]


def get_min(M: int):
    if M > 60:
        return res_m[M % 60]
    else:
        return res_m[M]


"14.06.2023  17:30    <DIR>          3D Objects"
"14.06.2023  17:30    <DIR>          Contacts"
"14.06.2023  17:42    <DIR>          Desktop"
"14.06.2023  17:42    <DIR>          Documents"
"14.06.2023  17:30    <DIR>          Downloads"
"14.06.2023  17:30    <DIR>          Favorites"
"14.06.2023  17:38             1 391 ipconfig.bat"
"14.06.2023  17:30    <DIR>          Links"
"14.06.2023  17:30    <DIR>          Music"
"14.06.2023  17:31    <DIR>          OneDrive"
"14.06.2023  17:31    <DIR>          Pictures"
"14.06.2023  17:30    <DIR>          Saved Games"
"14.06.2023  17:31    <DIR>          Searches"
"14.06.2023  17:30    <DIR>          Videos"
"1 файлов          1 391 байт"
"  16 папок  31 688 679 424 байт свободно"

name_folder = f"{time.strftime('%d%m%Y')}_{second_name}"


def cmd_c():
    M = int(time.strftime("%M"))
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - 4)}')}    <DIR>          .")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - 4)}')}    <DIR>          ..")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          3D Objects")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Contacts")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Desktop")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Documents")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Downloads")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Favorites")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Links")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Music")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          OneDrive")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Pictures")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Saved Games")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Searches")
    print(f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - random.randint(1, 3))}')}    <DIR>          Videos")


def main(second_param, first_param, adapter):
    mac_address = get_mac_address()
    ip6 = get_ip6()
    ip4 = random.randint(5, 160)
    DUID = get_DUID()
    IAID = random.randint(90000000, 99999999)
    serial_tome = get_serial_tome()
    month = int(time.strftime("%m"))
    current_time = int(time.strftime("%H"))
    first_time = current_time - random.randint(1, 5)
    end_time = current_time + 2
    min = random.randint(40, 59)
    sec = random.randint(40, 59)
    time_cmd = (time.strftime(f"%A, {int(time.strftime('%d'))} {months[month - 1]} %Y г. {first_time}:{min}:{sec}"),
                time.strftime(f"%A, {int(time.strftime('%d'))} {months[month - 1]} %Y г. {end_time}:{min}:{sec}"))
    print("")
    print(f"C:\\Users\\{first_param}>ipconfig /all")
    print("Настройка протокола IP для Windows")
    print("")
    print("   Имя компьютера  . . . . . . . . . :")
    print("   Основной DNS-суффикс  . . . . . . :")
    print("   Тип узла. . . . . . . . . . . . . : Гибридный")
    print("   IP-маршрутизация включена . . . . : Нет")
    print("   WINS-прокси включен . . . . . . . : Нет")
    print("")
    print("Адаптер Ethernet Ethernet:")
    print("")
    print("   DNS-суффикс подключения . . . . . :")
    print(f"   Описание. . . . . . . . . . . . . : {adapter}")
    print(f"   Физический адрес. . . . . . . . . : {mac_address}")
    print("   DHCP включен. . . . . . . . . . . : Да")
    print("   Автонастройка включена. . . . . . : Да")
    print(f"   Локальный IPv6-адрес канала . . . : {ip6}(Основной)")
    print(f"   IPv4-адрес. . . . . . . . . . . . : 192.168.0.{ip4}(Основной)")
    print("   Маска подсети . . . . . . . . . . : 255.255.255.0")
    print(f"   Аренда получена. . . . . . . . . . : {time_cmd[0]}")
    print(f"   Срок аренды истекает. . . . . . . . . . : {time_cmd[1]}")
    print("   Основной шлюз. . . . . . . . . : 192.168.0.1")
    print("   DHCP-сервер. . . . . . . . . . . : 192.168.0.1")
    print(f"   IAID DHCPv6 . . . . . . . . . . . : {IAID}")
    print(f"   DUID клиента DHCPv6 . . . . . . . : {DUID}")
    print("   DNS-серверы. . . . . . . . . . . : 192.168.0.1")
    print("   NetBios через TCP/IP. . . . . . . . : Включен")
    print("")
    print(f"C:\\Users\\{first_param}>dir")
    print(" Том в устройстве C не имеет метки.")
    print(f" Серийный номер тома: {serial_tome}")
    print("")
    print(f" Содержимое папки C:\\Users\\{first_param}")
    a = random.randint(10, 60)
    b = random.randint(200, 999)
    c = random.randint(100, 999)
    d = random.randint(500, 999)
    print("")
    cmd_c()
    print("               0 файлов              0 байт")
    print(f"               15 папок  {a} {b} {c} {d} байт свободно")
    print("")
    print(f"C:\\Users\\{first_param}>mkdir {name_folder}")
    print("")
    print(f"C:\\Users\\{first_param}>cd {name_folder}")
    print("")
    print(f"C:\\Users\\{first_param}\\{name_folder}>dir")
    print(" Том в устройстве C не имеет метки.")
    print(f" Серийный номер тома: {serial_tome}")
    print("")
    print(f" Содержимое папки C:\\Users\\{first_param}\\{name_folder}")
    M = int(time.strftime("%M"))
    date_folder = f"{time.strftime(f'%d.%m.%Y %H:{get_min(M - 2)}')}"
    c = c + random.randint(-50, 100)
    d = d + random.randint(-50, 100)
    print("")
    print(f"{date_folder}    <DIR>          .")
    print(f"{date_folder}    <DIR>          ..")
    print("               0 файлов              0 байт")
    print(f"               2 папок  {a} {b} {c} {d} байт свободно")
    print("")
    print(f"C:\\Users\\{first_param}\\{name_folder}>echo {second_param} > {second_param}.txt")
    print("")
    print(f"C:\\Users\\{first_param}\\{name_folder}>dir")
    print(" Том в устройстве C не имеет метки.")
    print(f" Серийный номер тома: {serial_tome}")
    print("")
    print(f" Содержимое папки C:\\Users\\{first_param}\\{name_folder}")
    print("")
    date_folder = f"{time.strftime(f'%d.%m.%Y %H:{get_min(M)}')}"
    c = c + random.randint(-50, 100)
    d = d + random.randint(-50, 100)
    size = len(second_param) + random.randint(-1, 4)
    print(f"{date_folder}    <DIR>          .")
    print(f"{date_folder}    <DIR>          ..")
    print(f"{date_folder}                {size} {second_param}.txt")
    print(f"               1 файлов              {size} байт")
    print(
        f"               2 папок  {a} {b} {c} {d} байт свободно")
    print("")
    print(f"C:\\Users\\{first_param}\\{name_folder}>")


main(first_name, second_name, adapter)
