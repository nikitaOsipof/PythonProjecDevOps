import itertools

# 1. itertools.count(start, step) — Бесконечный счетчик
# Аналог range(), но у него нет конечной точки. Он будет выдавать числа бесконечно с заданным шагом.
counter = itertools.count(start=10, step=5)

print(next(counter))  # Выведет: 10
print(next(counter))  # Выведет: 15
print(next(counter))  # Выведет: 20

# 2. itertools.cycle(iterable) — Бесконечный круг
# Принимает любой перебираемый объект (список, строку) и зацикливает его до бесконечности.
# Когда элементы заканчиваются, он просто начинает сначала.
# Зацикливаем список из трех элементов
spin = itertools.cycle(['один', 'два', 'три'])

for _ in range(5):
    print(next(spin))

# 3. itertools.repeat(object, times=None) — Бесконечный повтор
# Бесконечно (или заданное количество times раз) выдает один и тот же объект.
lazy_repeat = itertools.repeat("Привет!")

print(next(lazy_repeat))  # Привет!
print(next(lazy_repeat))  # Привет!


# Безопасная работа с бесконечными ленивыми потоками

# islice не копирует данные в память, а отрезает нужный кусок лениво, на лету
# бесконечный ленивый счетчик
infinite_counter = itertools.count(start=10, step=10)

# Безопасно отрезаем первые 5 элементов.
# В этот момент никаких вычислений еще не произошло
lazy_slice = itertools.islice(infinite_counter, 5)

# Вычисления происходят только здесь, при обертывании в list() или в цикле for:
print(list(lazy_slice))  # Выведет: [10, 20, 30, 40, 50]

# Паттерн take: получение первых N элементов
def take(n, iterable):
    """Возвращает первые n элементов итератора в виде списка."""
    return list(itertools.islice(iterable, n))

# Бесконечный круговой итератор
colors = itertools.cycle(['red', 'green', 'blue'])

# Безопасно берем 7 элементов из бесконечного цикла
print(take(7, colors))  # Выведет: ['red', 'green', 'blue', 'red', 'green', 'blue', 'red']

# itertools.takewhile()
#Если вы не знаете точное число N, сколько элементов вам нужно отрезать, но знаете условие, при котором нужно
# остановиться, используйте takewhile. Он будет брать элементы из бесконечного потока до тех пор, пока условие истинно.
infinite_squares = (x**2 for x in itertools.count())

# Будет брать числа из потока, пока они строго меньше 50
under_fifty = itertools.takewhile(lambda x: x < 50, infinite_squares)

print(list(under_fifty))  # Выведет: [0, 1, 4, 9, 16, 25, 36, 49]
