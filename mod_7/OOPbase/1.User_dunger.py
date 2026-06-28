'''
Представление сущности предметной области с магическими методами (dunder-методами, double underscore — двойное подчёркивание)

 dunger-методы позволяют вашим классам интегрироваться в синтаксис самого языка:
 объекты ваших типов можно было складывать с помощью +, сравнивать ==, передавать в функцию len() или выводить на экран print()
'''
class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role

    # Что будет в print() или в интерфейсе
    def __str__(self) -> str:
        return f"Пользователь {self.username} (Роль: {self.role})"

    # Что будет при отладке (например, внутри списка)
    def __repr__(self) -> str:
        return f"User(username='{self.username}', role='{self.role}')"

# Проверяем работу:
userA = User("Niko", "admin")
userM = User("Miko", "manager")

print(userA)        # Сработает __str__ -> Выведет: Пользователь Niko (Роль: admin)
print(repr(userA))  # Сработает __repr__ -> Выведет: User(username='Niko', role='admin')

users_list = [userA, userM]
print(users_list)  # Внутри коллекций Python ВСЕГДА вызывает __repr__
