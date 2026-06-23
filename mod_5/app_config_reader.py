#!/usr/bin/env python3
"""
Безопасный парсер конфигураций деплоя
Требуется: Написать отказоустойчивую утилиту, которая пытается прочитать список параметров для деплоя из YAML-файла.
Если файл поврежден или отсутствует, скрипт должен залогировать ошибку в файл app.log
и вернуть стандартные («безопасные») настройки.
"""
import logging
import yaml

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_deploy_config(filepath):
    default_config = {
        "environment": "development",
        "replicas": 1,
        "debug": True,
    }
    try:
        with open(filepath, "r") as f:
            config_data = yaml.safe_load(f)
            # Защита от пустого файла (yaml.safe_load вернет None)
            if config_data is None:
                return default_config
            return config_data
    except FileNotFoundError:
        logging.error(f"Конфигурационный файл '{filepath}' не найден. Применены дефолтные настройки.")
        return default_config
    except yaml.YAMLError as e:
        logging.error(f"Ошибка синтаксиса в файле '{filepath}': {e}. Применены дефолтные настройки.")
        return default_config

if __name__ == "__main__":
    print("Тест 1 (Нет файла):", load_deploy_config("missing_file.yaml"))
    print("Тест 2 (Поврежден):", load_deploy_config("broken.yaml"))

