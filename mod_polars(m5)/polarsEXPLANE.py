import duckdb
import polars as pl
import numpy as np
from datetime import datetime, timedelta

# 1. Генерируем 100 000 заказов в Polars
np.random.seed(42)
n_rows = 100_000

# Создаем массив меток времени (datetime) с шагом в 1 час
start_dt = datetime(2026, 1, 1, 0, 0)
end_dt = start_dt + timedelta(hours=n_rows - 1)

polars_orders = pl.DataFrame({
    # user_id: 100 000 случайных ID от 1 до 1000
    "user_id": np.random.randint(1, 1000, n_rows),
    # amount: 100 000 случайных сумм от 100 до 5000
    "amount": np.random.randint(100, 5000, n_rows),
    # date: генерируем сетку datetime и берем нужный срез
    "date": pl.datetime_range(start_dt, end_dt, "1h", eager=True)[:n_rows]
})

# 2. Справочник пользователей (1000 уникальных ID)
polars_users = pl.DataFrame({
    "user_id": list(range(1, 1001)),
    "country": np.random.choice(["Russia", "Kazakhstan", "Belarus", "China"], 1000)
})

# 3. Инициализируем контекст DuckDB
con = duckdb.connect()

# 4. Запрос с EXPLAIN ANALYZE (фильтр тоже изменен на datetime)
query_explain = """
    EXPLAIN ANALYZE
    SELECT 
        o.user_id, 
        u.country, 
        SUM(o.amount) as total_spend
    FROM polars_orders AS o
    JOIN polars_users AS u ON o.user_id = u.user_id
    WHERE o.date >= '2026-01-05 00:00:00'
    GROUP BY o.user_id, u.country
"""

# Выводим дерево на экран

# Стало (правильный вывод дерева):
# 1. Запускаем запрос


# 2. Печатаем чистый текст, который отформатировал DuckDB
print(con.execute(query_explain).fetchone()[1])


