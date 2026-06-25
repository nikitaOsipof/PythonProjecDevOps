#!/usr/bin/env python3
"""
точка входа
"""
# Импортируем функцию из субмодуля нашего нового пакета
from infrastructure.parser import load_deploy_config

if __name__ == "__main__":
    print("Проверка 1 (файл отсутствует):")
    config_1 = load_deploy_config("non_existent_file.yaml")
    print("Результат:", config_1)

    print("\nПроверка 2 (файл поврежден):")
    # Создадим битый файл для теста
    with open("corrupted.yaml", "w") as f:
        f.write("{broken_yaml: : [}")

    config_2 = load_deploy_config("corrupted.yaml")
    print("Результат:", config_2)
