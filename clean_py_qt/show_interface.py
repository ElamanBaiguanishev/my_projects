import telnetlib
import socket
import time

import requests

# Замените следующие переменные на актуальные значения
router_address = "my.keenetic.net"  # URL-адрес вашего модема или роутера
router_port = 23  # Порт Telnet
timeout = 5  # Время ожидания ответа (в секундах)
username = "admin"  # Имя пользователя для доступа к роутеру
password = "1234"  # Пароль для доступа к роутеру


def reload_port():
    try:
        # Разрешаем DNS-имя в IP-адрес
        router_ip = socket.gethostbyname(router_address)

        # Создаем объект Telnet
        tn = telnetlib.Telnet(router_ip, router_port, timeout=timeout)

        # Если подключение установлено успешно, то выведем сообщение об этом
        # print(f"Успешно подключено к {router_address} ({router_ip}:{router_port})")

        # print(all_result)

        tn.read_until(b"Login: ")
        # Отправляем имя пользователя
        tn.write(username.encode('ascii') + b"\n")

        # Ожидаем приглашение на ввод пароля
        tn.read_until(b"Password: ")
        # Отправляем пароль
        tn.write(password.encode('ascii') + b"\n")

        tn.read_until(b"(config)> ")

        command = "interface CdcEthernet0 usb power-cycle 60000\n"
        tn.write(command.encode('ascii'))

        time.sleep(60)

        tn.read_until(b"(config)> ")
        command = "show interface CdcEthernet0\n"
        tn.write(command.encode('ascii'))

        response = tn.read_until(b"(config)> ").decode('ascii')

        # Выведите ответ на экран
        print(response)

        # Закрываем соединение
        tn.close()

        return True
    except socket.gaierror as e:
        print(f"Не удалось разрешить DNS-имя {router_address}: {str(e)}")
        return False
    except Exception as e:
        print(f"Не удалось подключиться к {router_address}: {str(e)}")
        return False


reload_port()
