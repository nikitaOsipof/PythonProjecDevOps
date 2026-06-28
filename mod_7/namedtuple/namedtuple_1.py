'''
Именнованные кортежи
https://docs.python.org/3/library/collections.html#namedtuple-factory-function-for-tuples-with-named-fields
'''

# удобно присваивать индексам имена

MANUFACTURER, MODEL, SEATING = (0, 1, 2) # последовательность справа распаковывается
MINIMUM, MAXIMUM = (0, 1)
aircraft = ("Airbus", "A320-200", (100, 220))
print(aircraft [SEATING] [MAXIMUM]) # аналогично aircraft[2][1]

# но удобнее использовать именованные кортежи
import collections
# Пример 1. Создаются объекты типа sale

Sale = collections.namedtuple("sale", "productid customerid date quantity price")
sales = []
sales.append(Sale(432, 921, "2018-09-14", 3, 7.99))
sales.append(Sale(419, 874, "2018-09-15", 1, 18.49))

total = 0
for sale in sales:
    total += sale.quantity * sale.price     # обращение к атрибутам
print("Total ${0:.2f}".format(total))

# Пример 2. Создаются объекты нескольких типов
Aircraft = collections.namedtuple("Aircraft", "manufacturer model seating")
Seating = collections.namedtuple("Seating", "minimum maximum")

aircraft = Aircraft("Airbus", "A320-200", Seating(100, 220))
print(aircraft.seating.maximum)