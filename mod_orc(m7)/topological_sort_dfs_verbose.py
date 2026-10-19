from collections import defaultdict


def topological_sort_dfs_verbose(n, edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    visited = [False] * n  # Вершина полностью обработана (черная)
    temp_mark = [False] * n  # Вершина в процессе обработки (серая)
    order = []  # Стек результата

    def visit(u, depth):
        indent = "  " * depth
        print(f"{indent}-> Вход в DFS({u})")

        if temp_mark[u]:
            print(f"{indent}   ОБНАРУЖЕН ЦИКЛ!")
            raise ValueError("Обнаружен цикл")

        if visited[u]:
            print(f"{indent}   Вершина {u} уже обработана. Возврат.")
            return

        # Помечаем как "серую" (в процессе)
        temp_mark[u] = True
        print(f"{indent}   Временная метка установлена. Идем к потомкам {adj[u]}.")

        # Рекурсивно обходим всех потомков
        for v in adj[u]:
            print(f"{indent}   |")
            print(f"{indent}   └─> Ребро {u} -> {v}")
            visit(v, depth + 1)

        # Откат (backtracking): все потомки обработаны
        temp_mark[u] = False
        visited[u] = True
        order.append(u)
        print(f"{indent}   <- Выход из DFS({u}). Добавляем в стек: {u}. Текущий стек: {order}")

    # Запускаем DFS из каждой вершины, чтобы покрыть несвязные компоненты
    for u in range(n):
        if not visited[u]:
            print(f"\nЗапуск обхода из корневой вершины {u}:")
            visit(u, 0)

    # Разворачиваем стек, чтобы получить порядок от истоков к стокам
    return order[::-1]


# --- Наш пример DAG ---
n_vertices = 5
graph_edges = [
    (0, 2),
    (0, 3),
    (1, 3),
    (1, 4),
    (2, 3),
    (3, 4)
]

print("Структура графа (список смежности):")
adj_demo = defaultdict(list)
for u, v in graph_edges:
    adj_demo[u].append(v)
for u in range(n_vertices):
    print(f"  {u} -> {adj_demo[u]}")

print("\n" + "=" * 50 + "\nПошаговый процесс обхода:\n" + "=" * 50)

result = topological_sort_dfs_verbose(n_vertices, graph_edges)
print(f"\nФинальный результат (разворот стека): {result}")