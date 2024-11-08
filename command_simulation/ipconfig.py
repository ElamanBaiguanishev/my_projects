import subprocess

# Запускаем команду ipconfig и захватываем ее вывод с указанием кодировки cp866
ipconfig_process = subprocess.Popen('ipconfig /all', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')
output, _ = ipconfig_process.communicate()

# Разделяем вывод на строки
output_lines = output.split('\n')

for line in output_lines:
    print(line)

# Ищем строку с информацией о сроке аренды
lease_info = None
for line in output_lines:
    if 'Срок аренды' in line:
        lease_info = line
        break

if lease_info:
    print("Информация о сроке аренды:", lease_info)
else:
    print("Информация о сроке аренды не найдена.")

# Закрываем процесс
ipconfig_process.kill()