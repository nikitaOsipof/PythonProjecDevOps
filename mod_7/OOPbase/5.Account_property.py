'''
Инкапсульция - защитить данные от некорректных значений
@property - рекомендуемый синтаксис доступа к полям
'''

class BankAccount:
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner
        # Обратите внимание на нижнее подчеркивание перед именем.
        # В Python префикс '_' намекает, что переменная "приватная" (внутренняя),
        # и трогать её напрямую снаружи класса не нужно.
        self._balance = initial_balance

    # 1. ГЕТТЕР (Чтение свойства)
    # Декоратор @property превращает метод balance() в свойство-геттер
    @property
    def balance(self) -> float:
        print("[СИСТЕМА] Проверка баланса...")
        return self._balance

    # 2. СЕТТЕР (Запись значения)
    # Имя декоратора должно строго совпадать с именем свойства: @имя_свойства.setter
    @balance.setter
    def balance(self, new_value: float):
        print(f"[СИСТЕМА] Попытка изменить баланс на: {new_value}")
        # Защита данных (Валидация):
        if new_value < 0:
            raise ValueError("Баланс счета не может быть отрицательным!")
        self._balance = new_value

    # 3. ДЕЛЕТЕР (Удаление свойства — используется редко, но полезно знать)
    @balance.deleter
    def balance(self):
        print("[СИСТЕМА] Сброс баланса счета.")
        self._balance = 0.0

    @property
    def full_info(self) -> str:
        return f"{self.owner} имеет баланс: {self._balance}"


# Создаем счет
account = BankAccount("Niko", 1000.0)

# ЧИТАЕМ баланс (Вызываем геттер без круглых скобок!)
# Нам не нужно писать account.get_balance()
print(account.balance)
# Выведет:
# [СИСТЕМА] Проверка баланса...
# 1000.0

# ИЗМЕНЯЕМ баланс (Вызываем сеттер через обычный знак равенства)
# Нам не нужно писать account.set_balance(1500.0)
account.balance = 1500.0
# Выведет: [СИСТЕМА] Попытка изменить баланс на: 1500.0

# ПОПЫТКА СЛОМАТЬ систему (Защита сработает!)
try:
    account.balance = -50.0
except ValueError as e:
    print(f"Ошибка перехвачена: {e}")  # Выведет: Баланс счета не может быть отрицательным!

print(account.full_info)

# УДАЛЯЕМ свойство (Вызываем делетер через ключевое слово del)
del account.balance
print(account.balance)  # Выведет: 0.0

account._balance = 10  # все равно работает, но не рекомендуется
print(account._balance)