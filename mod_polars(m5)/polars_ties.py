'''
В Polars при ранжировании одинаковых значений (коллизий / ties) аргумент method определяет,
как именно будут распределяться места.
'''
import polars as pl

df = pl.DataFrame({
    "product": ["A", "B", "C", "D", "E"],
    "price": [100, 80, 80, 80, 50]  # Три одинаковых цены
})

# Применим все доступные методы ранжирования по убыванию цены
ranks_df = df.with_columns(
    pl.col("price").rank("dense", descending=True).alias("dense"),
    pl.col("price").rank("min", descending=True).alias("min"),
    pl.col("price").rank("max", descending=True).alias("max"),
    pl.col("price").rank("average", descending=True).alias("average"),
    pl.col("price").rank("ordinal", descending=True).alias("ordinal")
)

print(ranks_df)
