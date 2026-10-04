'''
Для того чтобы скользящее среднее работало по реальным временным интервалам (например, ровно за последние 7 дней),
а не просто по количеству строк, в Polars используется метод .rolling_mean_by().
'''

import numpy as np
import polars as pl
import plotly.express as px

# 1. Генерируем временной ряд с ИСКУССТВЕННЫМИ ПРОПУСКАМИ дат
np.random.seed(42)
num_days = 365

# Генерируем непрерывный год
full_dates = pl.date_range(
    start=pl.date(2023, 1, 1),
    end=pl.date(2023, 12, 31),
    interval="1d",
    eager=True,
)

df_clean = pl.DataFrame({
    "date": full_dates,
    "sales": np.random.randint(100, 1000, len(full_dates))
})

# Симулируем реальную жизнь: случайно удаляем 20% дней (пропуски в данных)
df_with_gaps = df_clean.sample(fraction=0.8, shuffle=False).sort("date")

# 2. Считаем скользящее среднее ПО ВРЕМЕНИ (через .rolling_mean_by)
df_analytics = df_with_gaps.with_columns([
    # Окно ровно в 7 календарных дней. Данные должны быть отсортированы по колонке "by".
    pl.col("sales")
    .rolling_mean_by(
        by="date",
        window_size="7d",
        closed="right"  # Окно включает текущий день и смотрит назад
    )
    .alias("rolling_mean_7_calendar_days"),

    # Окно ровно в 30 календарных дней
    pl.col("sales")
    .rolling_mean_by(
        by="date",
        window_size="30d",
        closed="right"
    )
    .alias("rolling_mean_30_calendar_days")
])

# 3. Визуализация в Plotly
df_long = df_analytics.unpivot(
    index="date",
    on=["sales", "rolling_mean_7_calendar_days", "rolling_mean_30_calendar_days"]
)

# Красивые названия для легенды
df_long = df_long.with_columns(
    pl.col("variable").replace({
        "sales": "Фактические продажи (с пропусками дат)",
        "rolling_mean_7_calendar_days": "7-дневный тренд по времени",
        "rolling_mean_30_calendar_days": "30-дневный тренд по времени"
    })
)

fig = px.line(
    df_long,
    x="date",
    y="value",
    color="variable",
    title="Временной скользящий тренд в Polars (.rolling_mean_by с учетом пропусков дат)",
    labels={"value": "Сумма", "date": "Дата"},
    template="plotly_white"
)

# Стилизация графиков для лекции
fig.update_traces(patch={"line": {"width": 1, "dash": "dot"}},
                  selector={"name": "Фактические продажи (с пропусками дат)"})
fig.update_traces(patch={"line": {"width": 3}}, selector={"name": "7-дневный тренд по времени"})
fig.update_traces(patch={"line": {"width": 4}}, selector={"name": "30-дневный тренд по времени"})

fig.show()
