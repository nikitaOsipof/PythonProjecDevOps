'''
Метод __getattribute__(self, name) вызывается ВСЕГДА при абсолютно любом обращении к атрибуту
используется (например, для создания систем логирования, систем защиты данных или ленивой загрузки объектов
'''

class StrictLogger:
    def __init__(self, username: str):
        self.username = username
        self.secret_token = "XYZ123"

    def __getattribute__(self, name: str):
        print(f"[ЛОГЕР] Кто-то пытается прочитать поле: {name}")

        # Защита конфиденциальных данных
        if name == "secret_token":
            raise PermissionError("Доступ к токену заблокирован системой безопасности!")

        # ПРАВИЛЬНЫЙ путь чтения полей: используем super() = защита от рекурсивного вызова
        return super().__getattribute__(name)


# Использование:
user = StrictLogger("Ivan")

print(user.username)  # Выведет лог и имя "Ivan"

try:
    print(user.secret_token)  # Сработает перехват и защита!
except PermissionError as e:
    print(f"Отказ: {e}")
