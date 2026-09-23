'''
Задача безопасности: в лог-файлы или консоль мониторинга нельзя выводить персональные данные клиентов
(номера телефонов или ID секретных токенов) в открытом виде.
Требуется написать декоратор маскирования, который будет перехватывать строковый ответ любой функции и скрывать его
 центральную часть символами ***.
'''
import time
from functools import wraps
from typing import Callable, Any


def mask_sensitive_output(func: Callable[..., str]) -> Callable[..., str]:
    """
    Классический декоратор. Принимает функцию, возвращающую строку,
    и маскирует её центральную часть для защиты данных.
    """

    @wraps(func)  # Гарантирует сохранение __name__ и __doc__ оригинальной функции
    def wrapper(*args: Any, **kwargs: Any) -> str:
        # 1. Выполняем оригинальную функцию и перехватываем её ответ
        raw_string = func(*args, **kwargs)

        print(f"[Служба ИБ] Перехвачена строка из функции '{func.__name__}'")

        # 2. Логика трансформации: маскируем символы
        if len(raw_string) > 6:
            masked = raw_string[:3] + "********" + raw_string[-3:]
        else:
            masked = "***"

        # 3. Возвращаем измененный результат наружу
        return masked

    return wrapper


# --- Демонстрация параметризованного декоратора (Фабрика декораторов) ---
def performance_monitor(threshold_sec: float) -> Callable:
    """
    Декоратор с аргументами. Проверяет время выполнения функции.
    Если функция работает дольше threshold_sec, выводит предупреждение.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            execution_time = time.perf_counter() - start_time

            if execution_time > threshold_sec:
                print(
                    f"[⚠️ СКОРОСТЬ] Внимание! '{func.__name__}' работала {execution_time:.4f} сек! (Лимит: {threshold_sec})")
            return result

        return wrapper

    return decorator


# --- Применение разработанных декораторов ---

@performance_monitor(threshold_sec=0.5)
@mask_sensitive_output
def generate_user_session_token(user_id: int) -> str:
    """Генерирует конфиденциальный токен сессии пользователя."""
    # Симулируем задержку при тяжелых вычислениях ключа
    time.sleep(0.6)
    return f"SECRET_SESSION_TOKEN_FOR_USER_ID_{user_id}_XYZ999"


if __name__ == "__main__":
    print("--- Старт теста безопасности системы ---")
    # Вызов функции активирует цепочку декораторов: Сначала замерится время, потом замаскируется вывод
    secure_token = generate_user_session_token(42)
    print(f"Итоговый токен для вывода на экран: {secure_token}")
