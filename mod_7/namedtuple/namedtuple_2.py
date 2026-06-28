''' collections.namedtuple - неизменяемый кортеж с именованными полями.'''
from collections import namedtuple
from datetime import datetime

# Определим тип прокси-сервера
Proxy = namedtuple("Proxy", ["ip", "port"])

# Укажим данные конкретного сервера
proxy1 = Proxy("192.168.1.100", 8080)

# проверим
print(proxy1.ip)    # '192.168.1.100'
print(proxy1.port)  # 8080

#Пример: лог-событие
LogEntry = namedtuple("LogEntry", ["timestamp", "service", "status"])

logs = [
    LogEntry(datetime.now(), "nginx", "active"),
    LogEntry(datetime.now(), "postgres", "inactive"),
]

for entry in logs:
    print(f"[{entry.timestamp}] {entry.service}: {entry.status}")



