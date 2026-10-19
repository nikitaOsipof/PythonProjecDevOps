
from graphlib import TopologicalSorter

# Описываем зависимости: ключ зависит от значений (значения должны быть выполнены РАНЕЕ)
# Например, 'clean_data' зависит от 'extract_orders'
dependencies = {
    "clean_data": {"extract_orders"},
    "enrich_profiles": {"clean_data"},
    "calc_metrics": {"enrich_profiles"},
    "send_slack_report": {"calc_metrics"}
}

# Инициализируем сортировщик
ts = TopologicalSorter(dependencies)

# Получаем строго линейный порядок для выполнения
linear_order = list(ts.static_order())
print("Порядок выполнения задач:")
print(" -> ".join(linear_order))
# Вывод: extract_orders -> clean_data -> enrich_profiles -> calc_metrics -> send_slack_report
