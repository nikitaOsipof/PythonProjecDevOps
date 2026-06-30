from datetime import datetime, timezone, timedelta
from unittest.mock import patch, mock_open
import pytest
import json
# Импортируем наши классы из основного скрипта (предположим, он называется main.py)
from ooptime import LogEntry, JsonLogParser, LogAnalyzer, BaseNotifier

# Устанавливаем фиксированную базовую точку времени (2026 год), относительно которой будем считать "сейчас"
MOCK_NOW = datetime(2026, 6, 27, 23, 0, 0, tzinfo=timezone.utc)


# ==========================================
# 1. ТЕСТЫ ДЛЯ КЛАССА LogEntry (Юнит-тесты)
# ==========================================

def test_json_log_parser_valid_standard_json():
    """Проверяем парсинг файла, валидного по стандарту JSON (массив на top-level)."""

    # ИСПРАВЛЕНО: Теперь это один валидный JSON-массив на верхнем уровне
    mock_file_content = json.dumps([
        {"remote_ip": "10.0.0.1", "status": 200, "timestamp": "2026-06-27T22:45:00Z"},
        {"remote_ip": "10.0.0.2", "status": 500, "timestamp": "2026-06-27T22:46:00Z"}
    ])

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        parser = JsonLogParser("standard_valid.json")
        entries = list(parser.iter_entries())

        # Ожидаем, что успешно распарсились оба элемента из массива
        assert len(entries) == 2

        # ИСПРАВЛЕНО: Корректный доступ к объектам внутри списка по индексам
        assert entries[0].ip == "10.0.0.1"
        assert entries[0].status_code == 200

        assert entries[1].ip == "10.0.0.2"
        assert entries[1].status_code == 500


def test_json_log_parser_broken_top_level():
    """Проверяем, что если JSON сломан на top-level, парсер безопасно возвращает пустой список."""

    # Невалидный JSON (пропущена закрывающая скобка массива на верхнем уровне)
    mock_file_content = '[{"remote_ip": "10.0.0.1", "status": 200, "timestamp": "2026-06-27T22:45:00Z"}'

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        parser = JsonLogParser("broken_top_level.json")
        entries = list(parser.iter_entries())

        # Из-за ошибки на top-level парсер должен безопасно вернуть пустой результат
        assert len(entries) == 0


# ==========================================
# 2. ТЕСТЫ ДЛЯ ПАРСЕРА (Использование Mock)
# ==========================================

def test_json_log_parser_valid_and_invalid_lines():
    """Проверяем, что парсер корректно разбирает JSON и игнорирует битые строки."""
    # Симулируем содержимое файла в памяти
    mock_file_content = (
        '{"remote_ip": "10.0.0.1", "status": 200, "timestamp": "2026-06-27T22:45:00Z"}\n'
        'БИТАЯ СТРОКА НЕ JSON\n'
        '{"remote_ip": "10.0.0.2", "status": 500, "timestamp": "2026-06-27T22:46:00Z"}\n'
    )

    # Исполняем тест, подменяя системную функцию open()
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        parser = JsonLogParser("fake_path.json")
        entries = list(parser.iter_entries())

        # Ожидаем, что успешно распарсились только 2 строки из 3
        assert len(entries) == 2
        assert entries[0].ip == "10.0.0.1"
        assert entries[0].status_code == 200
        assert entries[1].ip == "10.0.0.2"
        assert entries[1].status_code == 500


# ==========================================
# 3. ТЕСТЫ ДЛЯ АНАЛИЗАТОРА (Бизнес-логика)
# ==========================================

class SpyNotifier(BaseNotifier):
    """Специальный тестовый класс (Spy), чтобы поймать отправленный отчет."""

    def __init__(self):
        self.sent_report = None

    def send_report(self, report_text: str):
        self.sent_report = report_text


@patch("main.datetime")  # Подменяем datetime внутри main.py, чтобы контролировать "текущее время"
def test_analyzer_time_filtering(mock_datetime):
    """Проверяем, что анализатор берет логи ТОЛЬКО за последние 5 минут."""
    # Фиксируем текущее время для теста: 23:00:00
    mock_datetime.now.return_value = MOCK_NOW
    mock_datetime.fromisoformat = datetime.fromisoformat

    # Готовим тестовые данные для парсера
    # 1. Ошибка 5 минут назад (ровно на границе) -> Должна войти
    entry_fresh_error = LogEntry("192.168.1.1", 500, MOCK_NOW - timedelta(minutes=5))
    # 2. Ошибка 6 минут назад -> Должна отсечься по времени
    entry_old_error = LogEntry("192.168.1.2", 502, MOCK_NOW - timedelta(minutes=6))
    # 3. Успешный запрос 1 минуту назад -> Должен отсечься, так как не ошибка
    entry_fresh_success = LogEntry("192.168.1.3", 200, MOCK_NOW - timedelta(minutes=1))

    # Создаем фальшивый парсер, возвращающий наши заготовленные объекты
    class StubParser:
        def iter_entries(self):
            return [entry_fresh_error, entry_old_error, entry_fresh_success]

    spy_notifier = SpyNotifier()
    analyzer = LogAnalyzer(parser=StubParser(), notifier=spy_notifier)

    # Запускаем анализ за последние 5 минут
    analyzer.analyze_recent_errors(minutes=5)

    # ПРОВЕРКИ (Asserts):
    # В отчете должен быть только IP 192.168.1.1 (так как он свежий и это ошибка)
    assert spy_notifier.sent_report is not None
    assert "192.168.1.1" in spy_notifier.sent_report

    # IP старой ошибки и успешного запроса быть не должно
    assert "192.168.1.2" not in spy_notifier.sent_report
    assert "192.168.1.3" not in spy_notifier.sent_report


@patch("main.datetime")
def test_analyzer_no_errors_message(mock_datetime):
    """Проверяем поведение системы, если ошибок вообще не обнаружено."""
    mock_datetime.now.return_value = MOCK_NOW

    class EmptyParser:
        def iter_entries(self):
            return []  # Логов нет

    spy_notifier = SpyNotifier()
    analyzer = LogAnalyzer(parser=EmptyParser(), notifier=spy_notifier)

    analyzer.analyze_recent_errors(minutes=5)

    assert spy_notifier.sent_report == "За последние 5 мин. ошибок не обнаружено."
