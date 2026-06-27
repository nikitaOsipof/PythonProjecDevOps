'''
Архитектура решения
    Форматы логов:
        TextLogParser — для стандартного текстового лога.
        JsonLogParser — для современного структурированного JSON-лога.
    Получатели отчетов:
        ConsoleNotifier — вывод в терминал.
        TelegramNotifier — отправка через API Telegram (или Slack/любой другой мессенджер).
'''
from collections import Counter
import json
import abc

# ==========================================
# 1. МОДЕЛЬ ДАННЫХ (ИНКАПСУЛЯЦИЯ)
# ==========================================

class LogEntry:
    """Единый объект строки лога для всей системы."""
    def __init__(self, ip: str, status_code: int):
        self.ip = ip
        self.status_code = status_code

    @property
    def is_error(self) -> bool:
        """Бизнес-логика определения ошибки инкапсулирована здесь."""
        return 400 <= self.status_code < 600


# ==========================================
# 2. ИНТЕРФЕЙСЫ И ПАРСЕРЫ (ПОЛИМОРФИЗМ)
# ==========================================

class BaseLogParser(abc.ABC):
    """Абстрактный класс (интерфейс) для всех будущих парсеров."""
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abc.abstractmethod
    def iter_entries(self):
        """Каждый парсер обязан реализовать этот метод как генератор."""
        pass


class TextLogParser(BaseLogParser):
    """Парсер для обычного текстового Nginx лога."""
    def iter_entries(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 9:
                    ip = parts[0]
                    status = int(parts[8]) if parts[8].isdigit() else 0
                    yield LogEntry(ip, status)


class JsonLogParser(BaseLogParser):
    """Парсер для логов в формате JSON (например, структурированный Vector/Fluentd)."""
    def iter_entries(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    # Извлекаем ключи из JSON структуры
                    ip = data.get("remote_ip", "")
                    status = int(data.get("status", 0))
                    yield LogEntry(ip, status)
                except (json.JSONDecodeError, ValueError):
                    # Пропускаем битые строки JSON
                    continue


# ==========================================
# 3. ИНТЕРФЕЙСЫ И ОТПРАВИТЕЛИ (СТРАТЕГИЯ)
# ==========================================

class BaseNotifier(abc.ABC):
    """Интерфейс для отправки результатов куда-либо."""
    @abc.abstractmethod
    def send_report(self, report_text: str):
        pass


class ConsoleNotifier(BaseNotifier):
    """Отправка отчета стандартно в консоль (stdout)."""
    def send_report(self, report_text: str):
        print("=== НАЧАЛО ОТЧЕТА В КОНСОЛЬ ===")
        print(report_text)
        print("=== КОНЕЦ ОТЧЕТА В КОНСОЛЬ ===")


class TelegramNotifier(BaseNotifier):
    """Отправка отчета в Telegram-чат через Webhook или API."""
    def __init__(self, token: str, chat_id: str):
        self.__token = token  # Скрываем sensitive данные
        self.__chat_id = chat_id

    def send_report(self, report_text: str):
        # Реальная DevOps-логика отправки. Имитируем через print для демо.
        print(f"[Telegram Bot] Отправка сообщения в чат {self.__chat_id}:")
        print(f"Текст:\n{report_text}")
        # Здесь был бы реальный вызов: requests.post(f"https://telegram.org{self.__token}/sendMessage", ...)


# ==========================================
# 4. ЯДРО СИСТЕМЫ (АНАЛИЗАТОР)
# ==========================================

class LogAnalyzer:
    """Анализатор, которому все равно, какой формат файла и куда слать ответ."""
    def __init__(self, parser: BaseLogParser, notifier: BaseNotifier):
        self.parser = parser       # Принимает любой парсер (наследник BaseLogParser)
        self.notifier = notifier   # Принимает любой нотификатор (наследник BaseNotifier)

    def analyze_and_notify(self, limit: int = 3):
        """Считает ошибки и автоматически отправляет отчёт в целевой источник."""
        error_counts = Counter()

        # Полиморфизм в действии: метод iter_entries работает для любого формата
        for entry in self.parser.iter_entries():
            if entry.is_error:
                error_counts[entry.ip] += 1

        # Формируем текст отчета
        report_lines = ["Топ IP-адресов со статус-ошибками:"]
        for ip, count in error_counts.most_common(limit):
            report_lines.append(f" - IP: {ip} -> Ошибок: {count}")

        report_text = "\n".join(report_lines)

        # Отправляем отчет через выбранную стратегию
        self.notifier.send_report(report_text)


# КЕЙС 1: Парсим JSON-лог -> Шлем результат в Telegram
json_parser = JsonLogParser("nginx.json")
tg_notifier = TelegramNotifier(token="SECRET_BOT_TOKEN", chat_id="12345678")

analyzer_tg = LogAnalyzer(parser=json_parser, notifier=tg_notifier)
analyzer_tg.analyze_and_notify()

print("\n" + "="*40 + "\n")

# КЕЙС 2: Парсим Текстовый-лог -> Выводим просто в консоль
text_parser = TextLogParser("nginx.log")
console_notifier = ConsoleNotifier()

analyzer_console = LogAnalyzer(parser=text_parser, notifier=console_notifier)
analyzer_console.analyze_and_notify()
