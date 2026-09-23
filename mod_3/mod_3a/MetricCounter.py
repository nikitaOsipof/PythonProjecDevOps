'''
для создания кэша данных или счетчика метрик, который хранит свое состояние между вызовами функции внутри конвейера
'''
class MetricCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0  # Состояние кэшируется внутри объекта класса

    def __call__(self, *args):
        self.count += 1
        print(f"[METRIC] Функция '{self.func.__name__}' вызвана {self.count} раз(а)")
        return self.func(*args)

# Применяем класс как декоратор
@MetricCounter
def download_api_page(page_num):
    return f"data_from_page_{page_num}"

# Вызываем функцию (на самом деле вызывается метод __call__ объекта MetricCounter)
print(download_api_page(12))
print(download_api_page(22))
