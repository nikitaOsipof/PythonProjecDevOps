'''
в Polars есть встроенный модуль SQLContext.
- парсит SQL-запрос,
- автоматически переводит его в Lazy-выражения Polars
- отправляет в родной оптимизатор Rust.
Это значит, что SQL-код получит все преимущества Predicate Pushdown и Projection Pushdown
'''
import polars as pl
from datetime import date


def run_polars_sql():
    print(f"Запуск встроенного SQL Polars. Версия: {pl.__version__}")

    # 1. Явно задаем даты объектами datetime.date (Polars 1.10 требование)
    polars_orders = pl.DataFrame({
        "user_id":[1, 2, 1, 3],
        "amount":[250, 400, 150, 700],
    "date": [date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3), date(2026, 1, 4)]
    })

    polars_users = pl.DataFrame({
        "user_id":[1,2,3],
        "country": ["Russia", "Kazakhstan", "Russia"]
    })

    # 2. Инициализируем контекст и регистрируем таблицы
    ctx = pl.SQLContext()
    ctx.register("orders", polars_orders)
    ctx.register("users", polars_users)

    # 3. Пишем SQL-запрос
    sql_query = """
        SELECT 
            o.user_id, 
            u.country, 
            SUM(o.amount) as total_spend
        FROM orders AS o
        JOIN users AS u ON o.user_id = u.user_id
        WHERE o.date >= '2026-01-01'
        GROUP BY o.user_id, u.country
    """

    # 4. Выполняем и собираем ленивый граф (.collect())
    analysis_result = ctx.execute(sql_query).collect()

    print("\nРезультат выполнения SQL-запроса:")
    print(analysis_result)


if __name__ == "__main__":
    run_polars_sql()
