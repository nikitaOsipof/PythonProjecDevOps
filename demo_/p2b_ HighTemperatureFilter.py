import random

# Имитируем «грязный» бесконечный поток данных с датчика (память = 0)
def raw_sensor_stream():
    while True:
        yield random.randint(20, 150)

class HighTemperatureFilter:
    """
    Класс-фильтр. Он является ИТЕРИРУЕМЫМ (Iterable),
    так как метод __iter__ возвращает генератор через yield.
    """

    def __init__(self, data_source, threshold=100):
        self.source = data_source  # Принимаем поток данных
        self.threshold = threshold

    def __iter__(self):
        # Вместо написания отдельного метода __next__ и ручного вызова next(),
        # пишем цикл с yield
        for current_value in self.source:
            if current_value > self.threshold:
                yield current_value  # Замораживает метод и отдает значение наружу


# --- ИСПОЛЬЗОВАНИЕ В ПАЙПЛАЙНЕ ---

raw_data = raw_sensor_stream()

# Создаем объект фильтра. Код внутри __iter__ еще НЕ начал выполняться
alert_system = HighTemperatureFilter(raw_data, threshold=120)

print("Запуск мониторинга через yield-класс (выведем первые 5):\n")

# Цикл for сам вызовет метод __iter__, получит генератор и начнет крутить его
for count, anomaly in enumerate(alert_system, 1):
    print(f"⚠️ Аномалия №{count}: Перегрев: {anomaly}°C!")

    if count == 5:
        print("\n[LOG] Мониторинг успешно завершен.")
        break
