import polars as pl

# Создаем тестовый датасет
data = pl.DataFrame({
    "category": ["Electronics", "Electronics", "Electronics", "Books", "Books", "Books"],
    "product": ["Phone", "Laptop", "Headphones", "Sci-Fi", "Drama", "Poetry"],
    "price": [1000, 1500, 200, 30, 25, 15]
})

lazy_df = data.lazy()

analysis = (
    lazy_df
    # 1. Считаем отношение текущей цены к средней в категории
    .with_columns(
        (pl.col("price") / pl.col("price").mean().over("category"))
        .alias("price_to_mean_ratio")
    )
    # 2. Правильное ранжирование: метод .rank() с параметром method="dense"
    .with_columns(
        pl.col("price").rank(method="dense", descending=True).over("category")
        .alias("rank")
    )
    # 3. Фильтруем ТОП-2 товара в каждой категории
    .filter(pl.col("rank") <= 2)
    # 4. Сортируем для вывода
    .sort(["category", "rank"])
)

print(analysis.collect())
print(pl.__version__)