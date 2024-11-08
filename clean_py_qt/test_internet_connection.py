import telnetlib
import time
import socket
import requests

# Замените следующие переменные на актуальные значения
router_address = "my.keenetic.net"  # URL-адрес вашего модема или роутера
router_port = 23  # Порт Telnet
timeout = 5  # Время ожидания ответа (в секундах)
username = "admin"  # Имя пользователя для доступа к роутеру
password = "1234"  # Пароль для доступа к роутеру


def get_external_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        response.raise_for_status()
        data = response.json()
        return data['origin']
    except requests.exceptions.RequestException:
        return None


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
        time.sleep(10)
        return True
    except socket.gaierror as e:
        print(f"Не удалось разрешить DNS-имя {router_address}: {str(e)}")
        return False
    except Exception as e:
        print(f"Не удалось подключиться к {router_address}: {str(e)}")
        return False


def main():
    start_time = time.time()
    reload_station()

    while True:
        external_ip = get_external_ip()
        if external_ip:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Интернет-соединение восстановлено через {elapsed_time:.2f} секунд. Ваш внешний IP: {external_ip}")
            break
        time.sleep(5)


if __name__ == "__main__":
    main()