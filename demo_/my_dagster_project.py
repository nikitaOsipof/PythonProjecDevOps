from dagster import asset, AssetExecutionContext, Definitions
from datetime import datetime


# АКТИВ 1: Сырые данные из API
@asset(
    group_name="ecom_pipeline",
    compute_kind="API_Call"
)
def raw_orders(context: AssetExecutionContext) -> list[dict]:
    """Скачивание свежих заказов из внешнего источника"""
    # Имитируем получение данных
    data = [
        {"order_id": 101, "amount": 250.0, "status": "completed"},
        {"order_id": 102, "amount": -50.0, "status": "fraud"},  # Ошибочная строка
        {"order_id": 103, "amount": 1400.0, "status": "completed"}
    ]
    context.log.info(f"Скачано {len(data)} записей.")
    return data


# АКТИВ 2: Очищенные данные. Зависит от raw_orders
# Dagster сам поймет зависимость, так как имя аргумента совпадает с именем функции выше!
@asset(
    group_name="ecom_pipeline",
    compute_kind="Python"
)
def cleaned_orders(context: AssetExecutionContext, raw_orders: list[dict]) -> list[dict]:
    """Фильтрация фродовых и ошибочных транзакций"""
    good_orders = [row for row in raw_orders if row["amount"] > 0]

    # Записываем метаданные прямо в актив для отслеживания в UI
    context.add_output_metadata(
        metadata={
            "total_records": len(raw_orders),
            "removed_records": len(raw_orders) - len(good_orders),
            "preview": good_orders[:1]
        }
    )
    return good_orders


# АКТИВ 3: Итоговая статистика (Витрина данных)
@asset(
    group_name="ecom_pipeline",
    compute_kind="PostgreSQL"
)
def sales_summary(context: AssetExecutionContext, cleaned_orders: list[dict]) -> dict:
    """Расчет агрегатов и сохранение в базу данных (имитация)"""
    total_revenue = sum(row["amount"] for row in cleaned_orders)

    summary = {
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "revenue": total_revenue,
        "order_count": len(cleaned_orders)
    }

    # Имитация SQL-запроса на перезапись данных (Идемпотентность)
    context.log.info(f"Данные успешно сохранены. Итоговая выручка: {total_revenue}")
    return summary


# 4. Объединяем все активы в единый репозиторий проекта
defs = Definitions(
    assets=[raw_orders, cleaned_orders, sales_summary]
)
