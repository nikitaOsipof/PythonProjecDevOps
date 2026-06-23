#!/usr/bin/env python3
"""
Практическая работа: Разработка генератора конфигураций .
"""


def generate_group_inventory(*hostnames, **shared_settings):
    """
    Функция принимает несколько имен хостов (*args) и общие настройки (**kwargs).
    Должна вернуть список строк конфигурации.

    Пример вывода для параметров ("web-01", "web-02", ansible_user="root"):
    [
        "web-01 ansible_user=root",
        "web-02 ansible_user=root"
    ]
    """
    inventory_lines = []

    # Настройки переводим в формат "ключ=значение" один раз для оптимизации
    settings_list = [f"{k}={v}" for k, v in shared_settings.items()]

    for host in hostnames:
        # Объединяем имя текущего хоста и все настройки
        line_parts = [host] + settings_list
        inventory_lines.append(" ".join(line_parts))

    return inventory_lines


def main():
    # Тестируем передачу нескольких хостов в *args и общих настроек в **kwargs
    web_group = generate_group_inventory(
        "web-server-01", "web-server-02", "web-server-03",
        ansible_user="ubuntu",
        env="production"
    )

    print("--- Группа Web ---")
    for line in web_group:
        print(line)

    # Тестируем группу баз данных (всего один хост, но логика должна сработать так же)
    db_group = generate_group_inventory(
        "db-primary",
        ansible_user="postgres",
        port=5432
    )

    print("\n--- Группа DB ---")
    for line in db_group:
        print(line)


if __name__ == "__main__":
    main()
