'''
В стиле ООП разделяем задачу на логические компоненты:
       строка лога (данные)
       арсер (процесс чтения)
       анализатор (бизнес-логика).
'''

from collections import Counter

class LogEntry:
    """Класс-контейнер для представления одной строки лога."""
    def __init__(self, raw_line: str):
        parts = raw_line.split()
        self.is_valid = len(parts) >= 9
        if self.is_valid:
            self.ip = parts[0]
            self.status_code = int(parts[8]) if parts[8].isdigit() else 0
        else:
            self.ip = ""
            self.status_code = 0

    @property
    def is_error(self) -> bool:
        """Инкапсулированная проверка: является ли статус ошибкой."""
        return 400 <= self.status_code < 600


class LogParser:
    """Класс для чтения и парсинга файла логов."""
    def __init__(self, file_path: str):
        self.file_path = file_path

    def iter_entries(self):
        """Генератор, который возвращает объекты LogEntry."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                entry = LogEntry(line)
                if entry.is_valid:
                    yield entry


class LogAnalyzer:
    """Класс для вычисления метрик и статистики."""
    def __init__(self, parser: LogParser):
        self.parser = parser

    def get_top_error_ips(self, limit: int = 3) -> list:
        """Считает топ IP-адресов, генерирующих ошибки."""
        error_counts = Counter()
        for entry in self.parser.iter_entries():
            if entry.is_error:
                error_counts[entry.ip] += 1
        return error_counts.most_common(limit)


# Использование кода:
parser = LogParser("access.log")
analyzer = LogAnalyzer(parser)

print("Топ IP-адресов с ошибками (ООП):")
for ip, count in analyzer.get_top_error_ips(3):
    print(f"IP: {ip} — Ошибок: {count}")

'''
Далее:
В каком формате хранятся логи? (обычный текст, JSON, CSV)
Куда нужно отправлять результаты анализа? (в консоль, в Telegram/Slack, или сохранять в базу данных)
Как расширить ООП-парсер под эти требования?
'''