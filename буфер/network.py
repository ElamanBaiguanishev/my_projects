import json
import telnetlib
import socket
import time
import requests

timeout = 5  # Время ожидания ответа (в секундах)
with open("resources/network.json") as json_file:
    data_json = json.load(json_file)
    interface = data_json["interface"]
    router_address = data_json["router_address"]
    router_port = int(data_json["router_port"])
    username = data_json["username"]
    password = data_json["password"]


def get_external_ip():
    count = 0
    while True:
        count += 1
        try:
            response_ = requests.get('https://httpbin.org/ip')
            response_.raise_for_status()
            data = response_.json()
            print("Попыток получения ip:", count)
            return data['origin']
        except:
            if count > 6:
                return None
            time.sleep(25)


def reload_station():
    try:
        print("Начинаю процесс перезагрузки станции")
        router_ip = socket.gethostbyname(router_address)
        tn = telnetlib.Telnet(router_ip, router_port, timeout=timeout)
        tn.read_until(b"Login: ")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        tn.read_until(b"(config)> ")
        command = "system reboot\n"
        tn.write(command.encode('ascii'))
        response = tn.read_until(b"(config)> ")  # Считываем ответ на команду
        tn.close()
        print(response.decode('ascii'))  # Выводим ответ на экран
        time.sleep(100)
        return True
    except socket.gaierror as e:
        print(f"Не удалось разрешить DNS-имя {router_address}: {str(e)}")
        return False
    except Exception as e:
        print(f"Не удалось подключиться к {router_address}: {str(e)}")
        return False


def reload_port():
    try:
        router_ip = socket.gethostbyname(router_address)
        tn = telnetlib.Telnet(router_ip, router_port, timeout=timeout)
        tn.read_until(b"Login: ")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        tn.read_until(b"(config)> ")
        command = f"interface {interface} usb power-cycle 60000\n"
        tn.write(command.encode('ascii'))
        time.sleep(60)
        tn.close()
        return True
    except socket.gaierror as e:
        print(f"Не удалось разрешить DNS-имя {router_address}: {str(e)}")
        return False
    except Exception as e:
        print(f"Не удалось подключиться к {router_address}: {str(e)}")
        return False


def change_ip():
    after_ip = get_external_ip()
    print("Ваш внешний IP-адрес:", after_ip)

    reload_port()

    before_ip = get_external_ip()

    if before_ip is None:
        reload_station()
        before_ip = get_external_ip()

    print("Ваш внешний IP-адрес:", before_ip)

    if after_ip != before_ip:
        return True
    else:
        return change_ip()


# counter = []
# i = 1
#
# try:
#     while True:
#         start_time = time.time()
#         print(f"{i} попытка:")
#         time_str_start = time.strftime("%H:%M:%S", time.localtime())
#         print("Старт в:", time_str_start)
#         change_ip()
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         print("Время выполнения функции:", elapsed_time, "секунд")
#         time_str_end = time.strftime("%H:%M:%S", time.localtime())
#         print("Конец в:", time_str_end)
#         counter.append(elapsed_time)
#         i += 1
#
# except KeyboardInterrupt:
#     if counter:
#         average_time = sum(counter) / len(counter)
#         print(f"Среднее время выполнения функции: {average_time:.2f} секунд")
#     else:
#         print("Нет данных для вычисления среднего времени.")
