import polars as pl


def gaming_analytics_demo():
    print("=== 1. Инициализация LazyFrame (Создание графа вычислений) ===")

    # заполненный датасет с тестовыми данными
    lazy_df = pl.DataFrame(
        {
            "nickname": [
                "Sniper1",
                "Sniper1",
                "Sniper1",
                "Healer_99",
                "Healer_99",
                "Healer_99",
                "WarriorX",
                "WarriorX",
            ],
            "match_id":[1, 1, 2, 2, 3, 3, 1, 2],
            "score":[500, 300, 450, 600, 200, 150, 400, 350],
            "is_win":[1, 0, 1, 1, 0, 0, 1, 0],
        }
    ).lazy()  # Переводим в ленивый режим (LazyFrame)

    # Формируем граф вычислений на движке Rust
    analytical_query = (
        lazy_df
        # Шаг 1: Добавляем скользящие и оконные метрики ДО фильтрации побед
        .with_columns(
            [
                # Оконная функция: доля очков игрока от общей суммы конкретного матча
                (
                    pl.col("score") / pl.col("score").sum().over("match_id") * 100
                ).alias("match_score_share"),
                # СКОЛЬЗЯЩЕЕ СРЕДНЕЕ: среднее по текущему и предыдущему матчу игрока
                pl.col("score")
                .rolling_mean(window_size=2, min_samples=1)
                .over("nickname")
                .alias("rolling_avg_score"),
            ]
        )
        # Шаг 2: Фильтруем только те сессии, которые закончились победой
        .filter(pl.col("is_win") == 1)
        # Шаг 3: Группируем по игрокам для поиска лидерской статистики
        .group_by("nickname")
        # Шаг 4: Агрегируем финальные метрики
        .agg(
            [
                pl.col("match_id").count().alias("total_wins"),
                pl.col("score").mean().alias("avg_win_score"),
                pl.col("match_score_share")
                .max()
                .alias("max_contribution_percent"),
                # Берем последнее актуальное скользящее среднее на момент победы
                pl.col("rolling_avg_score").last().alias("last_rolling_avg"),
            ]
        )
        # Шаг 5: Сортируем топ-игроков по количеству побед
        .sort("total_wins", descending=True)
    )

    print("\n=== 2. Печать графа вычислений (Сам запрос еще не выполнялся) ===")
    print(analytical_query.explain())


    # --- ДЕМОНСТРАЦИЯ ОТЛАДКИ ---

    print("=== [ОТЛАДКА] Тестирование графа через .head(n).collect() ===")
    # .head(3) сообщает оптимизатору Polars, что нам нужны только первые 3 строки источника
    debug_table = analytical_query.head(3).collect()
    print(debug_table)
    print(
        "💡 Обратите внимание: Это новый стандарт отладки в Polars. "
        "Оптимизатор Slice Pushdown автоматически ограничит чтение данных в самом начале."
    )


    print("\n=== 3. Выполнение графа через .collect() ===")
    result_table = analytical_query.collect()
    print(result_table)


if __name__ == "__main__":
    gaming_analytics_demo()
