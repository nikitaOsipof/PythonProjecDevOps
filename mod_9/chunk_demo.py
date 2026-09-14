'''
паттерн Chunking
Построчное чтение средствами Python (подходит для текстовых логов и CSV)
'''
import itertools

def process_chunk(chunk):
    """Контекст обработки отдельного кусочка данных."""
    # Здесь данные материализуются в ОЗУ, но только в объеме ОДНОГО чанка
    cleaned_lines = [line.strip().upper() for line in chunk if line.strip()]
    print(f"[CHUNK] Обработано строк: {len(cleaned_lines)} -> {cleaned_lines}")

def read_in_chunks(file_path, chunk_size=2):
    """Лениво читает файл блоками по chunk_size строк."""
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            # Отрезаем ленивый слайс от файлового итератора
            chunk_iterator = itertools.islice(file, chunk_size)

            # Проверяем, есть ли элементы в чанке.
            # peek делает первый шаг, поэтому собираем в список
            first_rows = list(itertools.islice(chunk_iterator, chunk_size))
            if not first_rows:
                break  # Файл закончился

            process_chunk(first_rows)


# Демонстрация: создадим временный файл и прочитаем его по кусочкам
with open("huge_logs.txt", "w") as f:
    f.write("user1,login\nuser2,logout\nuser3,click\nuser4,purchase\nuser5,view")

read_in_chunks("huge_logs.txt", chunk_size=2)
