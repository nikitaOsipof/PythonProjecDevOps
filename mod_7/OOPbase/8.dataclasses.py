from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0  # Можно задавать значения по умолчанию

'''
uv и Python автоматически сгенерируют три магических метода:
1.	__init__ 
2.	__repr__ 
3.	__eq__ 
'''
# Проверяем работу авто-генерации:
p1 = Product("Смартфон", 30000.0, 2)
p2 = Product("Смартфон", 30000.0, 2)

print(p1)       # Сработал авто-__repr__ -> Выведет: Product(name='Смартфон', price=30000.0, quantity=2)
print(p1 == p2) # Сработает авто-__eq__   -> Выведет: True

'''
Особенности дата - классов
1. Неизменяемые объекты(Защита данных)
флаг frozen = True
Такой объект ведет себя как кортеж(tuple)
'''
@dataclass(frozen=True)
class ImmutableUser:
    username: str
    user_id: int

user = ImmutableUser("Niko", 42)
# user.username = "Alex" # ❌ Вызовет ошибку FrozenInstanceError
'''
2. Тонкая настройка полей через field()
'''
from dataclasses import dataclass, field

@dataclass
class Order:
    order_id: int
    # default_factory=list гарантирует, что у каждого заказа будет СВОЙ уникальный список
    items: list[str] = field(default_factory=list)
    # repr=False скроет этот пароль из логов при вызове print(order)
    password_hash: str = field(default="123", repr=False)

'''
3. Пост-инициализация: Метод __post_init__
Если после заполнения полей нужно провести валидацию данных или вычислить дополнительное поле
'''
@dataclass
class Employee:
    first_name: str
    last_name: str
    email: str = field(init=False)  # Говорим, что email не нужно передавать в конструктор

    def __post_init__(self):
        # Генерируем email автоматически на основе имени
        self.email = f"{self.first_name.lower()}.{self.last_name.lower()}@company.com"

        # Проверяем корректность данных
        if not self.first_name:
            raise ValueError("Имя не может быть пустым")
'''
4. Генерация методов для сравнения - флаг order=True
'''
from dataclasses import dataclass

@dataclass(order=True)
class Player:
    # Важно: сравнение будет происходить по очереди, начиная с первого поля!
    score: int
    name: str

p1 = Player(score=100, name="Niko")
p2 = Player(score=250, name="Alex")

print(p1 < p2)  # True! (Сравнились значения score: 100 < 250)

'''
5. Чтобы объект можно было положить в множество set() или использовать как ключ в словаре dict, у него должен быть 
вычисляемый хэш (метод __hash__) - вы сделаете класс неизменяемым с помощью флага frozen=True, 
'''
@dataclass(frozen=True)
class Point:
    x: int
    y: int

pt = Point(10, 20)

# Теперь это легально:
my_set = {pt}         # Объект можно положить в множество!
my_dict = {pt: "Ок"}  # Объект может быть ключом словаря!
