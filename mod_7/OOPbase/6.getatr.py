'''
Метод __getattr__(self, name) вызывается Python только тогда, когда запрашиваемый атрибут НЕ БЫЛ НАЙДЕН стандартными способами
 (его нет ни в __init__, ни в методах класса).

  Пример: Умный JSON-объект
  Cкачали из API JSON-словарь настроек.
  Обращаться к нему по ключам config["server"]["port"] неудобно и длинно.
  Сделаем класс-обертку, который позволит обращаться к ключам словаря как к обычным свойствам через точку: config.port.
'''


class DynamicConfig:
    def __init__(self, data_dict: dict):
        # Сохраняем исходный словарь во внутреннее поле
        self._data = data_dict

    # Перехватываем обращение к любым отсутствующим полям
    def __getattr__(self, name: str):
        print(f"[ПЕРЕХВАТ] Поля '{name}' нет в классе. Ищу его в JSON-словаре...")

        if name in self._data:
            return self._data[name]

        # Если ключа нет и в словаре, генерируем стандартную для Python ошибку
        raise AttributeError(f"Объект 'DynamicConfig' не имеет атрибута '{name}'")


# Использование:
api_data = {"host": "127.0.0.1", "port": 8080, "timeout": 30}
config = DynamicConfig(api_data)
print(config.__dict__)
# Поле 'host' физически не объявлено в классе, но код сработает!
print(config.host)
# Выведет:
# [ПЕРЕХВАТ] Поля 'host' нет в классе. Ищу его в JSON-словаре...
# 127.0.0.1
print(config.__dict__)