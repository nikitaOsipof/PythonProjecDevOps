import itertools
import sys

# Шаг 1: Бесконечный генератор кубов (память = 0)
def infinite_cubes():
    acc = 1
    while True:
        yield acc ** 3
        acc += 1

 #Шаг 2: Функция-батчер, которая нарезает ЛЮБОЙ поток на пачки
def batch_stream(iterable, batch_size):
    # Превращаем входящие данные в итератор, если они им не являлись
    iterator = iter(iterable)
    while True:
        # islice берет ровно batch_size элементов, не двигая весь остальной поток
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch  # Возвращаем один контролируемый список (пачку)


# --- ДЕМОНСТРАЦИЯ ---

cubes_stream = infinite_cubes()
# Задаем жесткий лимит: размер одной пачки — 5 элементов
CHUNK_SIZE = 5

# Наш батчер — это тоже ленивый генератор! Память всё еще чиста.
batched_cubes = batch_stream(cubes_stream, CHUNK_SIZE)

print("Начинаем симуляцию пакетной записи в базу данных:\n")

# Имитируем работу пайплайна (например, обработку первых 4 пачек)
for step, chunk in enumerate(batched_cubes):
    if step >= 4:
        print("... и так далее до бесконечности без угрозы OOM ...")
        break

    # Внутри 'chunk' сейчас лежит обычный безопасный Python-список
    print(f"Пакет №{step + 1}: Получена пачка данных: {chunk}")
    print(f"Размер этой пачки в RAM: {sys.getsizeof(chunk)} байт.")
    print("-> Выполняем команду: INSERT INTO database VALUES (...)\n")
