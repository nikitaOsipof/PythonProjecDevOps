import sys
from typing import Literal
from loguru import logger

# Современный Type Hinting
LogRecord = dict[str, str | int]

def parse_log_line(line: str) -> LogRecord | None:
    """Парсит строку лога. Использует Pattern Matching (Python 3.10+)."""
    parts = line.strip().split(" | ")
    
    # Демонстрация pattern matching для инженерии данных
    match parts:
        case [timestamp, "INFO" | "DEBUG" as level, message]:
            return {"timestamp": timestamp, "level": level, "message": message}
        case [timestamp, "ERROR" as level, message, error_code]:
            return {"timestamp": timestamp, "level": level, "message": message, "code": int(error_code)}
        case _:
            return None

def main() -> None:
    logger.info("Запуск коллектора логов...")
    
    raw_logs = [
        "2026-05-16 12:00:00 | INFO | Пайплайн Polars успешно запущен",
        "2026-05-16 12:01:05 | ERROR | Ошибка подключения к PostgreSQL | 500",
        "2026-05-16 12:02:10 | INVALID_LINE_FORMAT"
    ]

    for line in raw_logs:
        result = parse_log_line(line)
        if result:
            logger.success(f"Успешно обработано: {result}")
        else:
            logger.warning(f"Битый лог отфильтрован: '{line}'")

if __name__ == "__main__":
    main()
