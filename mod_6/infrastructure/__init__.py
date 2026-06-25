#!/usr/bin/env python3
"""
логер
"""
import logging

# TODO: Настроить глобальный логгер для всего пакета.
# Конфигурация должна записывать сообщения уровня ERROR и выше в файл 'infrastructure.log'
# Формат записи: Время - Имя модуля - Уровень - Сообщение

logging.basicConfig(
    filename="infrastructure.log",
    level=logging.ERROR,
    format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
)

# Выведем отладочное сообщение, чтобы зафиксировать момент инициализации пакета
logging.warning("Пакет 'infrastructure' успешно инициализирован.")
print("Пакет 'infrastructure' успешно инициализирован.")