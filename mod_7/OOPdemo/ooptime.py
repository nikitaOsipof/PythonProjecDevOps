from collections import Counter
from datetime import datetime, timedelta, timezone
import json
import abc


# ==========================================
# 1. МОДЕЛЬ ДАННЫХ С ПОДДЕРЖКОЙ ВРЕМЕНИ
# ==========================================

class LogEntry:
    def __init__(self, ip: str, status_code: int, timestamp: datetime):
        self.ip = ip
        self.status_code = status_code
        self.timestamp = timestamp  # Теперь у каждой записи есть datetime объект

    @property
    def is_error(self) -> bool:
        return 400 <= self.status_code < 600


# ==========================================
# 2. ИНТЕРФЕЙС И JSON-ПАРСЕР
# ==========================================

class BaseLogParser(abc.ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abc.abstractmethod
    def iter_entries(self):
        pass


class JsonLogParser(BaseLogParser):
    """Парсер для честного, валидного JSON-файла (массива объектов)."""

    def iter_entries(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                # Читаем и парсим весь файл целиком на верхнем уровне
                log_data = json.load(file)

                # Проверяем, что на top-level пришел именно список
                if isinstance(log_data, list):
                    for item in log_data:
                        ip = item.get("remote_ip", "")
                        status = int(item.get("status", 0))

                        raw_time = item.get("timestamp", "").replace("Z", "+00:00")
                        dt = datetime.fromisoformat(raw_time)

                        yield LogEntry(ip, status, dt)
            except (json.JSONDecodeError, ValueError, KeyError):
                # Если весь JSON-файл поломан на top-уровне, выходим
                return


# ==========================================
# 3. ИНТЕРФЕЙС И ОТПРАВИТЕЛЬ
# ==========================================

class BaseNotifier(abc.ABC):
    @abc.abstractmethod
    def send_report(self, report_text: str):
        pass


class ConsoleNotifier(BaseNotifier):
    def send_report(self, report_text: str):
        print(report_text)


# ==========================================
# 4. АНАЛИЗАТОР С ФИЛЬТРАЦИЕЙ ПО ВРЕМЕНИ
# ==========================================

class LogAnalyzer:
    def __init__(self, parser: BaseLogParser, notifier: BaseNotifier):
        self.parser = parser
        self.notifier = notifier

    def analyze_recent_errors(self, minutes: int = 5, limit: int = 3):
        """Анализирует только ошибки за последние N минут."""
        error_counts = Counter()

        # Определяем временную границу (работаем в UTC)
        now = datetime.now(timezone.utc)
        time_threshold = now - timedelta(minutes=minutes)

        for entry in self.parser.iter_entries():
            # Фильтр 1: Запись должна быть свежее, чем порог времени
            # Фильтр 2: Запись должна быть ошибкой
            if entry.timestamp >= time_threshold and entry.is_error:
                error_counts[entry.ip] += 1

        if not error_counts:
            self.notifier.send_report(f"За последние {minutes} мин. ошибок не обнаружено.")
            return

        report_lines = [f"Топ IP-адресов с ошибками за последние {minutes} минут:"]
        for ip, count in error_counts.most_common(limit):
            report_lines.append(f" - {ip}: {count} раз(а)")

        self.notifier.send_report("\n".join(report_lines))


log_path = "nginx.json"

parser = JsonLogParser(log_path)
notifier = ConsoleNotifier()  #

analyzer = LogAnalyzer(parser, notifier)
# Проверяем строго окно в 5 минут
analyzer.analyze_recent_errors(minutes=5)