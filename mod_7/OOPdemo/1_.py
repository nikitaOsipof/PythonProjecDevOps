'''
Требуется прочитать лог-файл веб-сервера, найти все строки с ошибками (HTTP-статусы 4xx и 5xx)
и собрать статистику: сколько раз встретился каждый IP-адрес.

Решение по 1 варианту:
Обычный стиль (Процедурный / Скриптовый)
'''

from collections import Counter
# https://docs.python.org/3/library/collections.html#counter-objects

log_file_path = "access.log"
error_counts = Counter()

# Читаем файл и сразу обрабатываем логику
with open(log_file_path, "r", encoding="utf-8") as file:
    for line in file:
        parts = line.split()
        if len(parts) < 9:
            continue

        ip = parts[0]
        status_code = parts[8]

        # Проверяем, является ли статус ошибкой (начинается с 4 или 5)
        if status_code.startswith(('4', '5')):
            error_counts[ip] += 1

# Выводим результат
print("Топ IP-адресов с ошибками:")
for ip, count in error_counts.most_common(3):
    print(f"IP: {ip} — Ошибок: {count}")
