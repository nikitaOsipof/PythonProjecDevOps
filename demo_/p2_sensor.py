import random
import time
from typing import Generator, Dict

def smart_home_sensor_stream(sensor_id: str) -> Generator[Dict[str, any], None, None]:
    """
    Генератор, симулирующий бесконечный поток телеметрии с датчика.
    Показывает концепцию заморозки состояния функции через yield
    """
    print(f"[Датчик {sensor_id}] Инициализация физического интерфейса...")
    step = 0
    current_temp = 22.0  # Исходная температура в комнате

    while True:
        step += 1
        # Симулируем плавное изменение температуры с редкими выбросами (сбоями)
        current_temp += random.uniform(-0.5, 0.5)

        # Раз в 15 шагов имитируем критический сбой оборудования (аномальный выброс)
        if step % 15 == 0:
            current_temp = 999.0

        # Замораживаем функцию и отдаем структурированные данные наружу
        yield {
            "sensor_id": sensor_id,
            "timestamp": time.time(),
            "temperature": round(current_temp, 2),
            "step_id": step
        }

        # После того как контекст возобновится, мы возвращаем температуру в норму
        if current_temp == 999.0:
            current_temp = 22.0


# Код конвейера обработки данных:
if __name__ == "__main__":
    # Инициализируем генератор. Ни один элемент еще не вычислен
    sensor_pipeline = smart_home_sensor_stream(sensor_id="WEATHER_XT_01")

    print("[Конвейер] Начинаем потоковую фильтрацию данных...")

    for packet in sensor_pipeline:
        # Обрабатываем данные строго по одной записи. В памяти нет архива измерений
        if packet["temperature"] > 50.0:
            print(f"[⚠️ WARNING] Шаг {packet['step_id']}: Зафиксирован аппаратный сбой датчика!")
        else:
            print(f"[Данные] Шаг {packet['step_id']}: Температура в норме: {packet['temperature']}°C")

        # Искусственно прервем бесконечный цикл на 20-м шаге для демонстрации
        if packet["step_id"] >= 20:
            print("[Конвейер] Демонстрационный лимит шагов исчерпан. Остановка.")
            break
