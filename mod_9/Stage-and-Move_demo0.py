import os
import shutil
import sqlite3
import uuid

# Имитация конфигурации путей
STAGE_DIR = "./data_staging_area"
DB_PATH = "analytics_production.db"


def init_environment():
    """Создаем чистую инфраструктуру для работы."""
    os.makedirs(STAGE_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                registration_date TEXT
            )
        """
        )


# --- 1. ФАЗА STAGE (Изолированное буферизованное сохранение) ---
def stage_incoming_data(chunk_data: list):
    """Принимает сырые данные из внешнего мира и дешево сохраняет их 'как есть'

    на диск. База данных на этом этапе вообще не трогается.
    """
    # Генерируем уникальное имя для файла во избежание конфликтов
    stage_filename = f"batch_{uuid.uuid4().hex}.csv"
    stage_filepath = os.path.join(STAGE_DIR, stage_filename)

    print(f"[STAGE] Получен чанк данных. Сохраняем в буфер: {stage_filename}")

    # Быстрая запись на диск без валидации схем базы данных
    with open(stage_filepath, "w", encoding="utf-8") as f:
        for row in chunk_data:
            f.write(f"{row['id']},{row['name']},{row['date']}\n")

    return stage_filepath


# --- 2. ФАЗА MOVE (Материализация и очистка) ---
def move_staged_to_production():
    """Сканирует стейдж-зону, быстро транзакционно переносит данные

    в финальные таблицы СУБД и очищает за собой буфер.
    """
    staged_files = [
        os.path.join(STAGE_DIR, f)
        for f in os.listdir(STAGE_DIR)
        if f.endswith(".csv")
    ]

    if not staged_files:
        print("[MOVE] Нет файлов в стейдже для перемещения.")
        return

    print(
        f"[MOVE] Запуск фазы переноса. Найдено файлов для импорта: {len(staged_files)}"
    )

    # Открываем ОДНУ транзакцию для максимальной скорости записи
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        for file_path in staged_files:
            try:
                # Читаем файл и импортируем пачкой (Bulk Insert)
                with open(file_path, "r", encoding="utf-8") as f:
                    parsed_rows = []
                    for line in f:
                        # Минимальная валидация на лету
                        row_data = line.strip().split(",")
                        if len(row_data) == 3:
                            parsed_rows.append(row_data)

                    # Быстрая вставка пакета строк
                    cursor.executemany(
                        "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
                        parsed_rows,
                    )

                # Если файл успешно импортирован — удаляем его из стейджа
                os.remove(file_path)
                print(f"[MOVE] Файл {os.path.basename(file_path)} успешно перенесен и удален.")

            except Exception as e:
                # Если один файл битый — транзакция БД откатит изменения по нему,
                # но сам файл останется в стейдже для ручного разбора (Retry/Dead Letter Queue)
                print(f"[ERROR] Ошибка при переносе файла {file_path}: {e}")

        conn.commit()


# --- ДЕМОНСТРАЦИЯ РАБОТЫ КОНВЕЙЕРА ---
if __name__ == "__main__":
    init_environment()

    # Имитируем поток данных из сети (два независимых батча)
    network_batch_1 = [
        {"id": "u1", "name": "Алексей", "date": "2026-09-10"},
        {"id": "u2", "name": "Мария", "date": "2026-09-11"},
    ]
    network_batch_2 = [
        {"id": "u3", "name": "Иван", "date": "2026-09-12"},
        {"id": "u4", "name": "Елена", "date": "2026-09-12"},
    ]

    # Шаг 1: Сгружаем всё в стейдж (сетевые операции завершены, данные в безопасности на диске)
    stage_incoming_data(network_batch_1)
    stage_incoming_data(network_batch_2)

    # Шаг 2: В любой удобный момент времени (например, по крону ночью)
    # запускаем быструю материализацию в СУБД
    move_staged_to_production()

    # Проверяем результат в продакшн-таблице
    with sqlite3.connect(DB_PATH) as conn:
        users = conn.execute("SELECT * FROM users").fetchall()
        print(f"\n[Финальный результат в БД]: {users}")

    # Очистка папки
    shutil.rmtree(STAGE_DIR)

