from collections import defaultdict


def topological_sort_dfs(n, edges):
    """
    Выполняет топологическую сортировку через рекурсивный DFS.

    :param n: Количество вершин (от 0 до n-1)
    :param edges: Список кортежей (u, v), где u -> v
    :return: Список вершин в топологическом порядке
    """
    # Строим список смежности
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    visited = [False] * n  # Вершина полностью обработана
    temp_mark = [False] * n  # Вершина в процессе обработки (для поиска циклов)
    order = []  # Стек результата

    def visit(u):
        """Рекурсивный обход."""
        if temp_mark[u]:
            # Если мы встретили вершину, которая уже в текущем стеке вызовов,
            # значит, мы вернулись назад и нашли цикл.
            raise ValueError("Обнаружен цикл: топологическая сортировка невозможна")

        if not visited[u]:
            temp_mark[u] = True
            # Сначала обходим всех потомков
            for v in adj[u]:
                visit(v)

            # Когда все потомки обработаны, помечаем вершину как завершенную
            temp_mark[u] = False
            visited[u] = True
            # И добавляем её в стек (результат)
            order.append(u)

    # Запускаем DFS из каждой непосещенной вершины
    for u in range(n):
        if not visited[u]:
            visit(u)

    # Вершины в списке 'order' лежат в обратном порядке (от стока к истоку),
    # поэтому разворачиваем его перед возвратом.
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

# Запуск
result = topological_sort_dfs(n_vertices, graph_edges)
print("Итоговый топологический порядок (DFS):", result)