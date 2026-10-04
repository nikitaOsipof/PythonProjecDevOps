import numpy as np
import polars as pl
import plotly.express as px

# 1. Генерируем реалистичные данные о продажах за год
np.random.seed(42)
num_days = 365

df = pl.DataFrame(
    {
        "date": pl.date_range(
            start=pl.date(2023, 1, 1),
            end=pl.date(2023, 12, 31),
            interval="1d",
            eager=True,
        ),
        # Генерируем случайные продажи от 100 до 1000 единиц
        "sales": np.random.randint(100, 1000, num_days),
    }
).sort("date")  # Важно! Данные ДОЛЖНЫ быть отсортированы хронологически

# 2. Считаем скользящее среднее с правильной обработкой первых дней (min_samples=1)
df_with_rolling = df.with_columns(
    [
        # Недельное окно сглаживания
        pl.col("sales")
        .rolling_mean(window_size=7, min_samples=1)
        .alias("rolling_mean_7d"),
        # Месячное окно сглаживания
        pl.col("sales")
        .rolling_mean(window_size=30, min_samples=1)
        .alias("rolling_mean_30d"),
    ]
)

# 3. Визуализация в Plotly
# Переводим в "длинный" формат для построения мульти-линейного графика
df_long = df_with_rolling.unpivot(
    index="date", on=["sales", "rolling_mean_7d", "rolling_mean_30d"]
)

# Переименуем категории в легенде для лучшей читаемости студентами
df_long = df_long.with_columns(
    pl.col("variable").replace(
        {
            "sales": "Ежедневные продажи (Шум)",
            "rolling_mean_7d": "7-дневное скользящее (Неделя)",
            "rolling_mean_30d": "30-дневное скользящее (Месяц)",
        }
    )
)

fig = px.line(
    df_long,
    x="date",
    y="value",
    color="variable",
    title="Анализ тренда продаж (Rolling Average в Polars)",
    labels={"value": "Объем продаж", "variable": "Метрика"},
    template="plotly_white",  # Чистый белый стиль графика для презентаций
)

# Делаем линию исходных продаж более тонкой и блеклой, а тренды — яркими и четкими
fig.update_traces(patch={"line": {"width": 1, "dash": "dot"}}, selector={"name": "Ежедневные продажи (Шум)"})
fig.update_traces(patch={"line": {"width": 3}}, selector={"name": "7-дневное скользящее (Неделя)"})
fig.update_traces(patch={"line": {"width": 4}}, selector={"name": "30-дневное скользящее (Месяц)"})

fig.show()
