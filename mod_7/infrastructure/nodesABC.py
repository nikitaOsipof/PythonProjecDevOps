'''
Создать абстрактный базовый класс для всех типов проверок (Агентов),
подмешать к ним миксин для автоматического сохранения результатов в JSON.
'''
from abc import ABC, abstractmethod
import json

class JsonSerializableMixin:
    def save_to_json(self, filepath):
        with open(filepath, "w") as f:
            # Превращаем атрибуты объекта в JSON-строку
            json.dump(self.__dict__, f, indent=4, ensure_ascii=False)
        print(f"📦 Данные объекта успешно сохранены в {filepath}")


class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def execute_check(self):
        pass


class WebAgent(BaseAgent, JsonSerializableMixin):
    def __init__(self, name, target_url):
        super().__init__(name)
        self.target_url = target_url
        self.status = "Not Checked"

    # Реализация обязательного контракта абстрактного класса
    def execute_check(self):
        print(f"🤖 Агент [{self.name}] запускает пинг {self.target_url}...")
        self.status = "UP"  # Имитация успешного ответа
