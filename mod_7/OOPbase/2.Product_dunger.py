"""
Оператор == вызывает метод __eq__.
"""
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    # Переопределяем логику оператора "=="
    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return False  # Если сравниваем с другим типом данных, они не равны
        return self.name == other.name and self.price == other.price

    # Переопределяем логику оператора "<" (меньше)
    def __lt__(self, other) -> bool:
        if not isinstance(other, Product):
            raise TypeError("Нельзя сравнить товар с этим типом данных")
        return self.price < other.price

p1 = Product("Ноутбук", 50000)
p2 = Product("Ноутбук", 50000)
p3 = Product("Мышь", 1500)

print(p1 == p2)  # True! Потому что значения полей одинаковые.
print(p3 < p1)   # True! Потому что 1500 < 50000.

'''
если переопределили методы __eq__ и __lt__, то можно сортировать списки объектов с помощью функции sorted(products_list) без дополнительных настроек
'''
