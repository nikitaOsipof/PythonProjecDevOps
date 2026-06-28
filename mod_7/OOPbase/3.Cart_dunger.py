'''
можно сделать так, чтобы ваш класс вел себя как стандартный список или словарь:
•	__len__ — позволяет передавать ваш объект в функцию len()
•	__getitem__ — позволяет получать данные из объекта по индексу или ключу через квадратные скобки obj[index].
'''
class Cart:
    """Класс корзины покупок"""
    def __init__(self):
        self.items = []

    def add_item(self, item_name: str):
        self.items.append(item_name)

    def __len__(self) -> int:
        return len(self.items)  # Возвращаем количество товаров

    def __getitem__(self, index: int) -> str:
        return self.items[index] # Позволяет брать товар по индексу: cart[0]

my_cart = Cart()
my_cart.add_item("Телефон")
my_cart.add_item("Чехол")

print(len(my_cart))  # Сработает __len__ -> Выведет: 2
print(my_cart[0])    # Сработает __getitem__ -> Выведет: Телефон
