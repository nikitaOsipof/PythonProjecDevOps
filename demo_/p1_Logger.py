'''
Пример создания кастомного регистратора событий (Logger), который открывает файл сессии,
автоматически записывает туда время начала и окончания работы скрипта, а также фиксирует, упал ли пайплайн с ошибкой
'''
import datetime
import sys
from typing import Optional, Type


class SessionDataLogger:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.file = None

    def __enter__(self):
        """Инициализация контекста: открываем файл на запись"""
        self.file = open(self.log_path, "a", encoding="utf-8")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file.write(f"[{timestamp}] --- СТАРТ СЕССИИ ОБРАБОТКИ ДАННЫХ ---\n")
        return self  # Возвращаем объект для работы внутри блока with

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[object]
    ) -> bool:
        """Закрытие контекста: фиксируем статус и гарантированно закрываем дескриптор"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            if self.file:
                if exc_type is not None:
                    # Если внутри блока with произошел сбой (например, ZeroDivisionError)
                    self.file.write(f"[{timestamp}] [КРИТИЧЕСКИЙ СБОЙ] Пайплайн упал. Ошибка: {exc_val}\n")
                else:
                    # Если всё прошло гладко
                    self.file.write(f"[{timestamp}] [УСПЕХ] Пайплайн успешно завершен.\n")

                self.file.write(f"[{timestamp}] --- КОНЕЦ СЕССИИ ---\n\n")
        finally:
            # Блок finally гарантирует, что файл закроется в любом случае,
            # даже если сам метод __exit__ споткнется об ошибку ввода-вывода
            if self.file:
                self.file.close()
                print("[Система] Дескриптор файла успешно освобожден.")

        # Возвращаем False, чтобы ошибка летела в оркестратор (Airflow) дальше
        return False


# Демонстрация работы на лекции:
if __name__ == "__main__":
    with SessionDataLogger("pipeline_history.log") as logger:
        print("Выполняются аналитические вычисления...")
        # Симулируем успешную работу
        logger.file.write("[Процесс] Обработана пачка №1\n")

        # Если здесь раскомментировать ошибку, контекст все равно закроется корректно:
        # 1 / 0
