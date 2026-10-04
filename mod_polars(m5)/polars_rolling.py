'''
Работа со скользящими окнами (например, скользящее среднее за последние 7 дней)
Для решения проблемы если в данных есть пропуски дней в Polars встроен движок динамических временных окон
с помощью метода group_by_dynamic() или rolling().

Задача:
 Посчитать скользящую сумму продаж за последние 3 дня (включая текущий день) индивидуально для каждого магазина.
 Обратите внимание, что даты идут неравномерно.
'''
import polars as pl
from datetime import date

# Данные с пропусками в датах
sales_data = pl.DataFrame({
    "store": ["Магазин А", "Магазин А", "Магазин А", "Магазин Б", "Магазин Б"],
    "date": [date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 5), date(2026, 1, 1), date(2026, 1, 3)],
    "revenue":[100, 200, 400, 500, 300]
})

# Для работы временных окон данные ОБЯЗАТЕЛЬНО должны быть отсортированы по времени
sales_data = sales_data.sort("date")

# Применяем rolling-фильтр с обновленным API
rolling_result = sales_data.rolling(
    index_column="date",      # Колонка-индекс времени
    period="3d",              # Размер окна (3 дня)
    group_by="store",         # Актуальный параметр группировки (вместо by)
    closed="both"             # Включать ли границы окна (обе стороны включительно)
).agg(
    pl.col("revenue").sum().alias("rolling_3d_sum")
)

print(rolling_result)


'''
Особенные случаи

Сценарий 1. Коллизии времени (Несколько продаж в одну и ту же дату/время)
В Polars временные коллизии разрешены по умолчанию.
'''
import polars as pl
from datetime import date

# Исходный датасет с коллизиями
df_collisions = pl.DataFrame({
    "store": ["Магазин А"] * 4,
    "date": [date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 2), date(2026, 1, 3)],
    "revenue": [100, 200, 300, 400]
}).sort("date")

# Считаем скользящее окно за 2 дня с актуальным API
result = df_collisions.rolling(
    index_column="date",
    period="2d",
    group_by="store",  # Было: by="store"
    closed="both"
).agg(
    pl.col("revenue").sum().alias("rolling_2d_sum"),
    pl.col("revenue").count().alias("rows_in_window")
)

print(result)

'''
Сценарий 2. Параметр every (Расчет скользящего окна с шагом)
'''
import polars as pl
from datetime import date

# Ежедневные данные
df_daily = pl.DataFrame({
    "date": pl.date_range(date(2026, 1, 1), date(2026, 2, 1), "1d", eager=True),
    "sales": [10] * 32
})

# Правильный подход: используем group_by_dynamic для шага 'every'
step_result = df_daily.group_by_dynamic(
    index_column="date",
    every="1w",     # Шаг, с которым двигается сетка (раз в неделю)
    period="14d",   # Глубина просмотра данных назад для каждой точки (14 дней)
).agg(
    pl.col("sales").sum().alias("sales_last_14_days")
)

print(step_result)
