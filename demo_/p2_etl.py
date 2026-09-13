'''
Дополнительное задание: «Построение отказоустойчивого ETL-конвейера (Hard)»
Требуется реализовать отказоустойчивый потоковый пайплайн для обработки транзакций интернет-магазина.
Источником данных служит «бесконечный» текстовый файл с грязными логами продаж, а приемником — база данных (в рамках задания имитируется запись пачками).
Пайплайн должен состоять из цепочки генераторов и соответствовать следующим требованиям:
1.	Звено 1 (Источник): читает строки из файла.
2.	Звено 2 (Валидация): фильтрует битые строки (где сумма покупки отрицательная или равна нулю).
3.	Звено 3 (Обогащение): добавляет к каждой транзакции поле налога (НДС 20%).
4.	Звено 4 (Батчер): группирует обработанные транзакции в пачки по N штук для эффективной пакетной записи.
5.	Отказоустойчивость: если в процессе записи очередной пачки в базу происходит сбой (например, база временно недоступна), пайплайн не должен падать по OOM или терять прогресс. Он должен использовать паттерн Stage-and-Move (запись во временный файл-черновик).
'''
import json
import os
import itertools

# Имитируем файл-источник с грязными транзакциями
RAW_LOGS = [
    '{"tx_id": 1, "amount": 100, "user": "alice"}',
    '{"tx_id": 2, "amount": -50, "user": "bob"}',      # Битый лог (отрицательный amount)
    '{"tx_id": 3, "amount": 250, "user": "charlie"}',
    '{"tx_id": 4, "amount": 0, "user": "david"}',       # Битый лог (нулевой amount)
    '{"tx_id": 5, "amount": 500, "user": "eve"}',
    '{"tx_id": 6, "amount": 120, "user": "frank"}',
    '{"tx_id": 7, "amount": 300, "user": "grace"}'
]

# --- ШАГ 1: ТОЧКА ВХОДА (УЖЕ РЕАЛИЗОВАНО) ---
def transaction_source():
    """ Имитирует построчное чтение из терабайтного файла """
    for line in RAW_LOGS:
        yield line

# ШАГ 2: Решение
def validate_transactions(source_stream):
    for line in source_stream:
        data = json.loads(line)
        if data.get("amount", 0) > 0:
            yield data

# ШАГ 3: Решение
def enrich_vat(valid_stream):
    for tx in valid_stream:
        tx["vat"] = tx["amount"] * 0.20
        yield tx

# ШАГ 4: Решение
def chunk_stream(enriched_stream, batch_size):
    iterator = iter(enriched_stream)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch

# --- ШАГ 5: АТОМАРНАЯ ЗАПИСЬ (STAGE-AND-MOVE) ---
def save_batch_safely(batch, target_file="production_db.txt"):
    """
    Реализует паттерн Stage-and-Move. Записывает пачку во временный файл,
    после чего атомарно «накатывает» её на финальный файл.
    """
    staging_file = f".tmp_stage_{random.randint(1000, 9999)}.tmp" if 'random' in globals() else ".tmp_stage.tmp"

    try:
        # Пишем черновик
        with open(staging_file, 'w', encoding='utf-8') as f:
            for tx in batch:
                f.write(json.dumps(tx) + "\n")

        # Атомарный коммит: склеиваем файлы на уровне ОС
        with open(target_file, 'a', encoding='utf-8') as prod_f, \
                open(staging_file, 'r', encoding='utf-8') as stage_f:
            prod_f.write(stage_f.read())

    finally:
        # В любом случае удаляем временный мусор с диска
        if os.path.exists(staging_file):
            os.remove(staging_file)

# --- ЗАПУСК КОНВЕЙЕРА ---
if __name__ == "__main__":
    import random # нужно для генерации имен временных файлов

    # TODO: Соберите цепочку генераторов воедино.
    # Размер пачки (batch_size) установите равным 2.

    print("Запуск ETL-процесса...")
    # ====== КОД СБОРКИ ПАЙПЛАЙНА ======
    # pipeline = ...
    # ==================================
    # СБОРКА: Решение
    stage1 = transaction_source()
    stage2 = validate_transactions(stage1)
    stage3 = enrich_vat(stage2)
    pipeline = chunk_stream(stage3, batch_size=2)
    # Имитация выполнения
    for batch in pipeline:
        save_batch_safely(batch)
        print(f"Успешно записан пакет: {batch}")
