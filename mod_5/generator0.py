#!/usr/bin/env python3
"""
Практическая работа: Разработка генератора конфигураций

    Функция принимает имя хоста и произвольные параметры.
    Должна вернуть строку в формате Ansible Inventory.
    Пример: web-01 ansible_host=10.0.0.1 ansible_user=root

    # TODO: Напишите логику.
    # 1. Создайте список, где первым элементом будет hostname.
    # 2. Пройдите циклом по kwargs и добавьте в список строки вида "ключ=значение".
    # 3. Объедините элементы списка через пробел с помощью " ".join() и верните результат.

"""


def generate_inventory_line(hostname, **kwargs):
    parts = [hostname]
    for key, value in kwargs.items():
        parts.append(f"{key}={value}")
    return " ".join(parts)


def main():
    # Тестируем передачу нескольких хостов в args и общих настроек в **kwargs
    # Тестирование генератора с разным набором параметров
    print(generate_inventory_line("web-server-01", ansible_host="192.168.1.10"))

    print(generate_inventory_line("db-prod", ansible_host="10.0.0.5", ansible_user="postgres", max_connections=200))

    print(generate_inventory_line("load-balancer", ansible_host="172.16.0.1", port=443, ssl=True))


if __name__ == "__main__":
    main()
