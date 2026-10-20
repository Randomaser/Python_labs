"""
Лабораторная работа № 9. Вариант 4.
Тип графа: дерево (m = n - 1, связный, неориентированный).
Задача: высота дерева (от корня 0) и число листьев.
Доп. И4: проверка двудольности раскраской в два цвета при BFS.
Сравнение представлений: матрица смежности и списки смежности.
"""

import os
import platform
import random
import statistics
import sys
import time
from collections import deque

import matplotlib.pyplot as plt


SIZES = [1000, 5000, 10_000]
MATRIX_MAX_N = 1000   # матрица на n = 5000 и 10 000 занимает сотни мегабайт, поэтому её не строим
REPEATS = 5
SEED = 42


class MatrixGraph:
    """Граф на матрице смежности. Память Θ(n²)."""

    def __init__(self, n: int):
        self.n = n
        self.matrix = [[0] * n for _ in range(n)]

    def add_edge(self, u: int, v: int) -> None:
        self.matrix[u][v] = 1
        self.matrix[v][u] = 1

    def neighbors(self, v: int) -> list[int]:
        row = self.matrix[v]
        return [u for u in range(self.n) if row[u]]


class ListGraph:
    """Граф на списках смежности. Память Θ(n + m)."""

    def __init__(self, n: int):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int) -> None:
        self.adj[u].append(v)
        self.adj[v].append(u)

    def neighbors(self, v: int) -> list[int]:
        return self.adj[v]


def random_tree(n: int, seed: int) -> list[tuple[int, int]]:
    """Случайное дерево на n вершинах: каждая новая вершина присоединяется к случайной предыдущей."""
    rng = random.Random(seed)
    return [(i, rng.randrange(i)) for i in range(1, n)]


def build(cls, n: int, edges: list[tuple[int, int]]):
    graph = cls(n)
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


def bfs(graph, start: int):
    """BFS: возвращает (расстояния, предки, цвета для проверки двудольности, конфликт)."""
    n = graph.n
    dist = [-1] * n
    parent = [-1] * n
    color = [-1] * n
    dist[start] = 0
    color[start] = 0
    bipartite = True
    queue = deque([start])
    while queue:
        v = queue.popleft()
        for u in graph.neighbors(v):
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                parent[u] = v
                color[u] = 1 - color[v]
                queue.append(u)
            elif color[u] == color[v]:
                bipartite = False
    return dist, parent, color, bipartite


def tree_statistics(graph, root: int = 0):
    """Высота дерева (макс. расстояние от корня) и число листьев (степень 1, кроме корня при n > 1)."""
    dist, _, _, _ = bfs(graph, root)
    height = max(dist)
    n = graph.n
    if n == 1:
        leaves = 1
    else:
        leaves = sum(1 for v in range(n) if len(graph.neighbors(v)) == 1 and v != root)
    return height, leaves


def measure(action, repeats: int = REPEATS):
    """Медиана времени action() по repeats запускам; возвращает (время, результат последнего запуска)."""
    times = []
    result = None
    for _ in range(repeats):
        started = time.perf_counter()
        result = action()
        times.append(time.perf_counter() - started)
    return statistics.median(times), result


def check_small_example() -> None:
    """Т1-подобная проверка на малом дереве и на цикле (проверка двудольности)."""
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    g = build(ListGraph, 6, edges)
    dist, parent, _, bip = bfs(g, 0)
    height, leaves = tree_statistics(g, 0)
    print("Малое дерево: рёбра", edges)
    print(f"  расстояния от 0: {dist}; предки: {parent}")
    print(f"  высота = {height}, листья = {leaves}, двудольно = {bip}")

    odd_cycle = build(ListGraph, 3, [(0, 1), (1, 2), (2, 0)])
    _, _, _, bip_cycle = bfs(odd_cycle, 0)
    print(f"Цикл из 3 вершин: двудольно = {bip_cycle} (ожидается False)")
    assert bip is True and height == 2 and leaves == 3 and bip_cycle is False


def experiment():
    """Сравнение представлений: время BFS, высота, листья, двудольность."""
    rows = []
    for n in SIZES:
        edges = random_tree(n, SEED + n)
        gl = build(ListGraph, n, edges)
        t_list, (height, leaves) = measure(lambda: tree_statistics(gl, 0))
        _, _, _, bip = bfs(gl, 0)
        assert bip is True, "дерево обязано быть двудольным"

        t_matrix = None
        if n <= MATRIX_MAX_N:
            gm = build(MatrixGraph, n, edges)
            t_matrix, (h_m, l_m) = measure(lambda: tree_statistics(gm, 0))
            assert (h_m, l_m) == (height, leaves)

        rows.append({"n": n, "height": height, "leaves": leaves, "bipartite": bip,
                     "t_list": t_list, "t_matrix": t_matrix})
    return rows


def save_chart(rows) -> None:
    out_dir = os.path.dirname(os.path.abspath(__file__))
    ns = [r["n"] for r in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(ns, [r["t_list"] for r in rows], "o-", label="Списки смежности")
    matrix_pts = [(r["n"], r["t_matrix"]) for r in rows if r["t_matrix"] is not None]
    plt.plot([p[0] for p in matrix_pts], [p[1] for p in matrix_pts], "s-", label="Матрица смежности")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n (логарифмическая шкала)")
    plt.ylabel("Время BFS + статистика, с")
    plt.title("Дерево: время обхода по представлениям")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr9_time.png"), dpi=160)
    plt.close()


def main() -> None:
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}\n")

    check_small_example()

    print("\nДерево: высота, листья, двудольность и время BFS (медиана 5 запусков)")
    rows = experiment()
    print(f"{'n':>7}{'высота':>9}{'листья':>9}{'двудольно':>12}{'списки, с':>13}{'матрица, с':>13}")
    for r in rows:
        matrix = f"{r['t_matrix']:.6f}" if r["t_matrix"] is not None else "не строилась"
        print(f"{r['n']:>7}{r['height']:>9}{r['leaves']:>9}{str(r['bipartite']):>12}"
              f"{r['t_list']:>13.6f}{matrix:>13}")

    save_chart(rows)
    print("\nГрафик сохранён: lr9_time.png")


if __name__ == "__main__":
    main()
