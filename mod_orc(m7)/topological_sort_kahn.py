from collections import defaultdict, deque


def topological_sort_kahn(n, edges):
    """
    Выполняет топологическую сортировку ориентированного ациклического графа
    с помощью алгоритма Кана.

    :param n: Количество вершин (от 0 до n-1)
    :param edges: Список кортежей (u, v), где u -> v
    :return: Список вершин в топологическом порядке
    """
    # 1. Строим список смежности и считаем степени входа
    adj = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    # 2. Инициализируем очередь вершинами со степенью входа 0
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    step = 0

    print(f"Шаг {step}: степени входа {in_degree}, очередь {list(queue)}, результат {order}")

    # 3. Основной цикл
    while queue:
        step += 1
        u = queue.popleft()
        order.append(u)

        print(f"Шаг {step}: извлекаем вершину {u}")

        # "Удаляем" вершину u и обновляем соседей
        for v in adj[u]:
            in_degree[v] -= 1
            print(f"  — уменьшаем in_degree[{v}] до {in_degree[v]}")
            # Если у соседа больше нет входящих рёбер, добавляем его в очередь
            if in_degree[v] == 0:
                queue.append(v)
                print(f"    -> добавляем вершину {v} в очередь")

        print(f"         текущее состояние очереди: {list(queue)}")
        print(f"         текущий результат: {order}\n")

    # 4. Проверка на циклы
    if len(order) != n:
        return None  # Граф содержит цикл

    return order


# --- пример DAG ---
# Вершины: 0, 1, 2, 3, 4
n_vertices = 5
graph_edges = [
    (0, 2),
    (0, 3),
    (1, 3),
    (1, 4),
    (2, 3),
    (3, 4)
]

# Запуск алгоритма
result = topological_sort_kahn(n_vertices, graph_edges)

if result is None:
    print("Ошибка: в графе обнаружен цикл. Топологическая сортировка невозможна.")
else:
    print("Итоговый топологический порядок:", result)