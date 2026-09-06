''' списки'''

# Список сервисов, которые нужно проверить
services_to_monitor = ["nginx", "docker", "postgresql"]

# Добавим ещё один
services_to_monitor.append("redis")

# Перебираем и проверяем
for service in services_to_monitor:
    print(service)

''' кортежи'''
# Пара значений: (IP, порт)
proxy = ("192.168.1.100", 8080)

# Список прокси-серверов
proxies = [
    ("10.1.1.1", 3128),
    ("10.1.1.2", 8080),
]

# Используем как ключ в словаре
proxy_cache = {("10.1.1.1", 3128): "OK"}

'''список vs кортеж: запуск задач'''
# Команда (tuple — фиксировано, безопасно)
base_command = ("rsync", "-avz")

# Динамические аргументы (list — можно дополнять)
source_paths = ["/home/user/data", "/etc/nginx"]

for src in source_paths:
    full_command = list(base_command) + [src, "/backup/"]
    print(full_command)


''' массивы'''
from array import array

# Массив таймингов запросов (в миллисекундах)
response_times = array('f', [123.4, 98.6, 110.2])

# Среднее время ответа
avg = sum(response_times) / len(response_times)

# Добавим новое значение
response_times.append(105.1)


