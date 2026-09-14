import os
import csv
import sqlite3
import logging
from typing import List, Dict

# Настройка логирования для мониторинга в продакшене
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Постоянные пути в системе
STAGE_DIR = "./data_staging_area"
DB_PATH = "analytics_production.db"


def init_warehouse():
    """Инициализация хранилища.

    Вызывается один раз при развертывании системы.
    Если база уже существует, этот код просто ничего не сделает.
    """
    os.makedirs(STAGE_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        # u_id — PRIMARY KEY, это гарантирует защиту от дубликатов (идемпотентность)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                u_id TEXT PRIMARY KEY,
                name TEXT,
                registration_date TEXT
            )
        """)
        conn.commit()
        logging.info("Хранилище проверено/инициализировано успешно.")
    finally:
        conn.close()


# --- 1. ФАЗА STAGE (Сбор сырых данных из внешних источников) ---
def stage_incoming_data(batch_id: str, chunk_data: List[Dict[str, str]]):
    """Принимает порцию данных от API/микросервиса и быстро сбрасывает на диск.

    База данных защищена от сетевого оверхеда.
    """
    stage_filename = f"batch_{batch_id}.csv"
    stage_filepath = os.path.join(STAGE_DIR, stage_filename)

    # Запись в локальный стейдж идет в режиме дозаписи/перезаписи конкретного батча
    with open(stage_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in chunk_data:
            writer.writerow([row['id'], row['name'], row['date']])

    logging.info(f"[STAGE] Батч {batch_id} успешно сохранен в буферную зону.")


# --- 2. ФАЗА MOVE (Транзакционный перенос данных в DWH) ---
def move_staged_to_production():
    """Сканирует буферную зону, переносит новые файлы в БД пачкой

    и очищает только обработанные временные файлы.
    """
    # Находим все CSV файлы, которые успели накопиться в стейдже
    staged_files = [
        os.path.join(STAGE_DIR, f)
        for f in os.listdir(STAGE_DIR)
        if f.endswith(".csv")
    ]

    if not staged_files:
        logging.info("[MOVE] Новых данных в стейдже не обнаружено. Выход.")
        return

    logging.info(f"[MOVE] Обнаружено файлов для импорта: {len(staged_files)}. Начинаем перенос...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        for file_path in staged_files:
            filename = os.path.basename(file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)

                # Паттерн Chunking: если файл внутри гигантский, читай его порциями
                # Для SQLite оптимально вставлять пачками по 50 000 строк
                while True:
                    # Считываем следующие 50 000 строк из файла
                    chunk = [row for _, row in zip(range(50000), reader)]
                    if not chunk:
                        break

                    # INSERT OR IGNORE — если данные этого пользователя уже были внесены ранее,
                    # они просто пропустятся, не вызывая ошибок и дубликатов.
                    cursor.executemany(
                        "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
                        chunk
                    )

            # Фиксируем изменения для этого файла
            conn.commit()

            # Файл успешно залит в БД — теперь его можно удалить ИЗ СТЕЙДЖА
            os.remove(file_path)
            logging.info(f"[MOVE] Файл {filename} успешно перенесен в БД и удален из буфера.")

    except Exception as e:
        # Если что-то пошло не так (например, файл заблокирован или поврежден),
        # откатываем незафиксированные изменения, но база остается жить!
        conn.rollback()
        logging.error(f"[CRITICAL] Сбой при обработке конвейера: {e}")
    finally:
        # Гарантированно закрываем соединение с базой в любом случае
        conn.close()


# --- РАБОТА СЕРВИСА В РЕАЛЬНЫХ УСЛОВИЯХ ---
if __name__ == "__main__":
    # 1. При старте контейнера/сервера проверяем структуру БД
    init_warehouse()

    # 2. Имитируем, что в течение дня в стейдж падали файлы (например, от вебхуков)
    data_morning = [{"id": "usr_101", "name": "Анна", "date": "2026-09-13"}]
    data_evening = [
        {"id": "usr_102", "name": "Борис", "date": "2026-09-13"},
        {"id": "usr_101", "name": "Анна", "date": "2026-09-13"}  # Дубликат для проверки идемпотентности
    ]

    stage_incoming_data(batch_id="morning_v1", chunk_data=data_morning)
    stage_incoming_data(batch_id="evening_v2", chunk_data=data_evening)

    # 3. Крон или оркестратор вызывает фазу перекладывания (Move)
    move_staged_to_production()

    # 4. База данныхanalytics_production.db осталась на диске.
    # При следующем запуске скрипта она продолжит наполняться.
