import sqlite3
from types import TracebackType
from typing import Optional, Type
import polars as pl


# =====================================================================
# 1. КОННЕКТОР К БД (Решение из Задания 1, оптимизированное для батчей)
# =====================================================================
class SQLiteDataConnector:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> "SQLiteDataConnector":
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> bool:
        if self.connection:
            try:
                if exc_type is not None:
                    self.connection.rollback()
                else:
                    self.connection.commit()
            finally:
                self.cursor.close()
                self.connection.close()
        return False

    def create_analytics_table(self) -> None:
        """Создание таблицы для хранения результатов анализа."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS leader_board (
                nickname TEXT PRIMARY KEY,
                total_wins INTEGER,
                avg_win_score REAL,
                max_contribution_percent REAL,
                last_rolling_avg REAL
            )
        """)

    def insert_batch(self, batch_data: list[tuple]) -> None:
        """Высокоскоростная пакетная вставка (Задание 1 + оптимизация)."""
        self.cursor.executemany(
            """
            INSERT OR REPLACE INTO leader_board 
            (nickname, total_wins, avg_win_score, max_contribution_percent, last_rolling_avg)
            VALUES (?, ?, ?, ?, ?)
            """,
            batch_data
        )


# =====================================================================
# 2. ДЕМОНСТРАЦИОННЫЙ СКРИПТ ДЛЯ ЛЕКЦИИ
# =====================================================================
def gaming_analytics_demo():
    # Исходный датасет
    lazy_df = pl.DataFrame({
        "nickname": ["Sniper1", "Sniper1", "Sniper1", "Healer_99", "Healer_99", "Healer_99", "WarriorX", "WarriorX"],
        "match_id":[1, 1, 2, 2, 3, 3, 1, 2],
        "score":[500, 300, 450, 600, 200, 150, 400, 350],
    "is_win": [1, 0, 1, 1, 1, 1, 0, 0]
    }).lazy()

    # Строим ленивый граф вычислений (синтаксис выражений)
    analytical_query = (
        lazy_df.with_columns([
            (pl.col("score") / pl.col("score").sum().over("match_id") * 100).alias("match_score_share"),
            pl.col("score").rolling_mean(window_size=2, min_samples=1).over("nickname").alias("rolling_avg_score")
        ])
        .filter(pl.col("is_win") == 1)
        .group_by("nickname")
        .agg([
            pl.col("match_id").count().alias("total_wins"),
            pl.col("score").mean().alias("avg_win_score"),
            pl.col("match_score_share").max().alias("max_contribution_percent"),
            pl.col("rolling_avg_score").last().alias("last_rolling_avg")
        ])
        .sort("total_wins", descending=True)
    )

    # -----------------------------------------------------------------
    # ВОПРОС 1: Проверка схемы (Schema) БЕЗ вычислений
    # -----------------------------------------------------------------
    print("=== ВОПРОС 1: Проверка схемы будущих данных ===")
    # Используем актуальный метод .collect_schema() вместо свойства .schema
    print(analytical_query.collect_schema())
    print("💡 Вычисления не производились. Polars вывел структуру плана через актуальный collect_schema().")


    # -----------------------------------------------------------------
    # ВОПРОС 2: Отладка без DeprecationWarning (head + collect)
    # -----------------------------------------------------------------
    print("\n=== ВОПРОС 2: Безопасная отладка графа (head + collect) ===")
    # За счет Slice Pushdown Polars прочитает только верхушку датасета
    debug_table = analytical_query.head(1).collect()
    print(debug_table)

    # -----------------------------------------------------------------
    # СБОРКА И ИНТЕГРАЦИЯ С БАЗОЙ ДАННЫХ (Пакетная вставка)
    # -----------------------------------------------------------------
    print("\n=== ФИНАЛ: Полный сбор данных и отправка батчем в SQLite ===")

    # 1. Получаем полный готовый DataFrame
    final_df = analytical_query.collect()
    print("Результат для сохранения:")
    print(final_df)

    # 2. Конвертируем данные в список кортежей для пакетной отправки
    # (iter_rows() работает лениво и эффективно передает строки)
    rows_to_insert = list(final_df.iter_rows())

    # 3. Записываем в базу данных одним запросом
    db_path = "gaming_stats.db"
    with SQLiteDataConnector(db_path) as db:
        db.create_analytics_table()
        db.insert_batch(rows_to_insert)
        print(f"🚀 Успешно сохранено пакетным запросом в файл базы данных: {db_path}")


if __name__ == "__main__":
    gaming_analytics_demo()
