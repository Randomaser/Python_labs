"""
Лабораторная работа № 10. Вариант 4.
1. Дейкстра в двух реализациях (линейный поиск минимума и двоичная куча)
   на разреженных графах с m ≈ 5n, n = 1000, 2000, 4000, веса 1..100.
2. К4: число кратчайших путей от источника до каждой вершины.
3. Расчёт критического пути сетевого графика проекта из 11 работ
   (топологическая сортировка Кана, прямой и обратный проходы).
"""

import heapq
import os
import platform
import random
import statistics
import sys
import time
from collections import deque

import matplotlib.pyplot as plt


INF = float("inf")
SIZES = [1000, 2000, 4000]
EDGE_FACTOR = 5        # m ≈ 5n
MAX_WEIGHT = 100
REPEATS = 3
SEED = 42


def dijkstra_array(adj, s):
    """Дейкстра с линейным поиском минимума. Трудоёмкость Θ(n²)."""
    n = len(adj)
    dist = [INF] * n
    parent = [-1] * n
    used = [False] * n
    dist[s] = 0
    for _ in range(n):
        v, best = -1, INF
        for i in range(n):
            if not used[i] and dist[i] < best:
                v, best = i, dist[i]
        if v == -1:
            break
        used[v] = True
        for u, w in adj[v]:
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                parent[u] = v
    return dist, parent


def dijkstra_heap(adj, s):
    """Дейкстра с двоичной кучей (heapq). Трудоёмкость O(m log n)."""
    n = len(adj)
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, v = heapq.heappop(heap)
        if d > dist[v]:
            continue                      # устаревшая запись в куче
        for u, w in adj[v]:
            if d + w < dist[u]:
                dist[u] = d + w
                parent[u] = v
                heapq.heappush(heap, (dist[u], u))
    return dist, parent


def count_shortest_paths(adj, s):
    """К4: число кратчайших путей от s до каждой вершины (Дейкстра + подсчёт в порядке извлечения)."""
    n = len(adj)
    dist = [INF] * n
    count = [0] * n
    dist[s] = 0
    count[s] = 1
    heap = [(0, s)]
    settled = [False] * n
    while heap:
        d, v = heapq.heappop(heap)
        if settled[v]:
            continue
        settled[v] = True
        for u, w in adj[v]:
            nd = d + w
            if nd < dist[u]:
                dist[u] = nd
                count[u] = count[v]
                heapq.heappush(heap, (nd, u))
            elif nd == dist[u]:
                count[u] += count[v]
    return dist, count


def restore_path(parent, target):
    """Восстановление пути по массиву предков."""
    path = []
    while target != -1:
        path.append(target)
        target = parent[target]
    return path[::-1]


def generate_graph(n: int, m: int, seed: int):
    """Случайный ориентированный взвешенный граф: остовное дерево для связности плюс случайные рёбра."""
    rng = random.Random(seed)
    adj = [[] for _ in range(n)]
    for i in range(1, n):
        j = rng.randrange(i)
        adj[j].append((i, rng.randint(1, MAX_WEIGHT)))
    extra = max(0, m - (n - 1))
    for _ in range(extra):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            adj[u].append((v, rng.randint(1, MAX_WEIGHT)))
    return adj


def measure(action, repeats: int = REPEATS):
    """Медиана времени action() по repeats запускам."""
    times = []
    result = None
    for _ in range(repeats):
        started = time.perf_counter()
        result = action()
        times.append(time.perf_counter() - started)
    return statistics.median(times), result


def topological_order(tasks):
    """Топологическая сортировка (алгоритм Кана). tasks: код -> (длительность, предшественники)."""
    indeg = {k: len(v[1]) for k, v in tasks.items()}
    succ = {k: [] for k in tasks}
    for k, (_, preds) in tasks.items():
        for p in preds:
            succ[p].append(k)
    queue = deque(sorted(k for k, d in indeg.items() if d == 0))
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for u in succ[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                queue.append(u)
    if len(order) != len(tasks):
        raise ValueError("Сетевой график содержит цикл: исходные данные некорректны")
    return order, succ


def critical_path(tasks):
    """Расчёт ES, EF, LS, LF, резервов и критических работ."""
    order, succ = topological_order(tasks)
    ES, EF = {}, {}
    for v in order:
        duration, preds = tasks[v]
        ES[v] = max((EF[p] for p in preds), default=0)
        EF[v] = ES[v] + duration
    T = max(EF.values())

    LS, LF = {}, {}
    for v in reversed(order):
        duration = tasks[v][0]
        LF[v] = min((LS[u] for u in succ[v]), default=T)
        LS[v] = LF[v] - duration

    reserve = {v: LS[v] - ES[v] for v in tasks}
    critical = [v for v in order if reserve[v] == 0]
    return T, ES, EF, LS, LF, reserve, critical


PROJECT = {
    "A": (5, []), "B": (7, ["A"]), "C": (4, ["B"]), "D": (6, ["B"]),
    "E": (10, ["C"]), "F": (9, ["D"]), "G": (3, ["E", "F"]),
    "H": (4, ["C", "D"]), "I": (6, ["G"]),
    "K": (3, ["G"]),                      # добавленная 11-я работа варианта 4
    "J": (2, ["H", "I", "K"]),
}


def check_small_graph() -> None:
    """Проверка на малом графе: сравнение реализаций, число путей, восстановление пути."""
    adj = [[] for _ in range(6)]
    for u, v, w in [(0, 1, 2), (0, 2, 2), (1, 3, 1), (2, 3, 1), (3, 4, 3), (1, 4, 6), (4, 5, 1)]:
        adj[u].append((v, w))
    d1, p1 = dijkstra_array(adj, 0)
    d2, p2 = dijkstra_heap(adj, 0)
    d3, cnt = count_shortest_paths(adj, 0)
    assert d1 == d2 == d3
    print("Малый граф: расстояния от 0:", d1)
    print("  число кратчайших путей:", cnt)
    print("  путь до 5:", " -> ".join(map(str, restore_path(p2, 5))))
    assert d1 == [0, 2, 2, 3, 6, 7]
    assert cnt[3] == 2
    assert restore_path(p2, 5) in ([0, 1, 3, 4, 5], [0, 2, 3, 4, 5])


def experiment_dijkstra():
    """Сравнение двух реализаций Дейкстры и подсчёт путей (К4) при разных n."""
    rows = []
    for n in SIZES:
        m = EDGE_FACTOR * n
        adj = generate_graph(n, m, SEED + n)
        t_arr, (d1, _) = measure(lambda: dijkstra_array(adj, 0))
        t_heap, (d2, p2) = measure(lambda: dijkstra_heap(adj, 0))
        assert d1 == d2
        _, cnt = count_shortest_paths(adj, 0)
        max_paths = max(cnt)
        rows.append({"n": n, "m": m, "t_arr": t_arr, "t_heap": t_heap, "max_paths": max_paths})
    return rows


def save_charts(rows):
    out_dir = os.path.dirname(os.path.abspath(__file__))
    ns = [r["n"] for r in rows]
    plt.figure(figsize=(8, 5))
    plt.plot(ns, [r["t_arr"] for r in rows], "o-", label="Линейный поиск минимума, Θ(n²)")
    plt.plot(ns, [r["t_heap"] for r in rows], "s-", label="Двоичная куча, O(m log n)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n (логарифмическая шкала)")
    plt.ylabel("Время, с (логарифмическая шкала)")
    plt.title("Дейкстра: m ≈ 5n, веса 1..100")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr10_dijkstra.png"), dpi=160)
    plt.close()


def main() -> None:
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}\n")

    check_small_graph()

    print("\nДейкстра: m = 5n, медиана 3 запусков")
    rows = experiment_dijkstra()
    print(f"{'n':>6}{'m':>8}{'массив, с':>13}{'куча, с':>12}{'отношение':>12}{'макс. чисел путей':>20}")
    for r in rows:
        print(f"{r['n']:>6}{r['m']:>8}{r['t_arr']:>13.4f}{r['t_heap']:>12.4f}"
              f"{r['t_arr'] / r['t_heap']:>12.1f}{r['max_paths']:>20}")
    save_charts(rows)

    print("\nКритический путь проекта (11 работ)")
    T, ES, EF, LS, LF, R, crit = critical_path(PROJECT)
    print(f"Длительность проекта: {T} дн.")
    print(f"{'Работа':>8}{'t':>5}{'ES':>5}{'EF':>5}{'LS':>5}{'LF':>5}{'Резерв':>8}{'Крит.':>7}")
    for v in sorted(PROJECT):
        print(f"{v:>8}{PROJECT[v][0]:>5}{ES[v]:>5}{EF[v]:>5}{LS[v]:>5}{LF[v]:>5}"
              f"{R[v]:>8}{'да' if R[v] == 0 else '':>7}")
    print("Критические работы:", " -> ".join(crit))
    print("\nГрафик сохранён: lr10_dijkstra.png")


if __name__ == "__main__":
    main()
