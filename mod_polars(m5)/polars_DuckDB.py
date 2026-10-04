import duckdb
import polars as pl

# 1. Заполняем DataFrame Polars тестовыми данными
polars_orders = pl.DataFrame({
    "user_id": [1, 2, 1, 3],
    "amount":[250, 400, 150, 700],
    "date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
})

polars_users = pl.DataFrame({
    "user_id":[1,2,3],
    "country": ["Russia", "Kazakhstan", "Russia"]
})

# 2. Инициализируем контекст DuckDB
con = duckdb.connect()

# 3. В SQL-запросе пишем имена НАШИХ ПЕРЕМЕННЫХ вместо названий файлов на диске!
query = """
    SELECT 
        o.user_id, 
        u.country, 
        SUM(o.amount) as total_spend
    FROM polars_orders AS o                   
    JOIN polars_users AS u ON o.user_id = u.user_id  
    WHERE o.date >= '2026-01-01'
    GROUP BY o.user_id, u.country
"""

# Выполняем запрос без обращений к диску — всё происходит в оперативной памяти
duck_rel = con.sql(query)

# Забираем результат обратно в Polars
final_features = duck_rel.pl()

print(final_features)
