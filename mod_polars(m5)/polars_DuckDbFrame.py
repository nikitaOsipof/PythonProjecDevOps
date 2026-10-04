'''
Прямой SQL-запрос из DuckDB к существующему в памяти объекту Polars
'''

import duckdb
import polars as pl

# 1. Создаем DataFrame в Polars (например, получили его после очистки или парсинга)
polars_sales = pl.DataFrame({
    "manager": ["Иван", "Мария", "Иван", "Елена", "Мария"],
    "product": ["Ноутбук", "Телефон", "Монитор", "Ноутбук", "Телефон"],
    "amount": [1200, 800, 400, 1500, 800]
})

# 2. Инициализируем контекст DuckDB
con = duckdb.connect()

# 3. Делаем SQL-запрос напрямую к переменной `polars_sales`!
# DuckDB автоматически найдет эту переменную в локальном окружении Python.
sql_query = """
    SELECT 
        manager,
        COUNT(product) AS total_orders,
        SUM(amount) AS total_revenue,
        AVG(amount) AS avg_check
    FROM polars_sales  
    GROUP BY manager
    HAVING SUM(amount) > 1000
    ORDER BY total_revenue DESC
"""

# 4. Выполняем запрос и возвращаем результат обратно в Polars DataFrame
analysis_result = con.sql(sql_query).pl()

print(analysis_result)

