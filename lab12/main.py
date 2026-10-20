"""
Лабораторная работа № 12. Вариант 4.
Задача: минимальная раскраска вершин графа (хроматическое число).
1. Точный метод: полный перебор с отсечением (возможная раскраска k цветами), размерности 8..12.
2. Конструктивная эвристика: жадная раскраска вершин в порядке убывания степеней.
3. Локальный поиск: перекраска вершин, уменьшающая число используемых цветов.
4. М4: отклонение эвристики от оптимума при n = 6, 7, 8, 9.
Эвристики дополнительно запускаются на графе из 200 вершин.
"""

import os
import platform
import random
import statistics
import sys
import time

import matplotlib.pyplot as plt


EXACT_SIZES = [8, 10, 12, 14, 16]
LARGE_N = 200
LARGE_DENSITY = 0.05
M4_SIZES = [6, 7, 8, 9]
M4_TRIALS = 30
DENSITY = 0.5
SEED = 42


def random_graph(n: int, density: float, seed: int):
    """Случайный неориентированный граф: список смежности (множества)."""
    rng = random.Random(seed)
    adj = [set() for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < density:
                adj[u].add(v)
                adj[v].add(u)
    return adj


def is_valid(adj, colors) -> bool:
    """Проверка корректности раскраски: соседние вершины имеют разные цвета."""
    return all(colors[u] != colors[v] for u in range(len(adj)) for v in adj[u])


def colorable_with(adj, k: int):
    """Точный метод: возможна ли раскраска k цветами (полный перебор с отсечением)."""
    n = len(adj)
    order = sorted(range(n), key=lambda v: -len(adj[v]))   # сначала вершины высокой степени
    colors = [-1] * n

    def backtrack(idx: int, used: int) -> bool:
        if idx == n:
            return True
        v = order[idx]
        for c in range(min(used + 1, k)):              # симметрия: новый цвет только следующий по порядку
            if all(colors[u] != c for u in adj[v]):
                colors[v] = c
                if backtrack(idx + 1, max(used, c + 1)):
                    return True
                colors[v] = -1
        return False

    if backtrack(0, 0):
        return True, colors
    return False, None


def exact_chromatic(adj):
    """Точный метод: минимальное k, при котором раскраска возможна. Перебор k от 1 вверх."""
    n = len(adj)
    if n == 0:
        return 0, []
    for k in range(1, n + 1):
        ok, colors = colorable_with(adj, k)
        if ok:
            return k, colors
    return n, list(range(n))


def greedy_by_degree(adj):
    """Конструктивная эвристика: вершины в порядке убывания степени, каждой — наименьший свободный цвет."""
    n = len(adj)
    order = sorted(range(n), key=lambda v: -len(adj[v]))
    colors = [-1] * n
    for v in order:
        taken = {colors[u] for u in adj[v] if colors[u] != -1}
        c = 0
        while c in taken:
            c += 1
        colors[v] = c
    return len(set(colors)), colors


def recolor_local_search(adj, colors, max_passes: int = 100):
    """Локальный поиск: перекраска вершин, при которой удаётся уменьшить число цветов.
    Пытаемся опустошить самый редкий цвет, переназначая его вершины по существующим цветам."""
    colors = colors[:]
    for _ in range(max_passes):
        used = sorted(set(colors))
        if len(used) <= 1:
            break
        # цвет с наименьшим числом вершин — кандидат на устранение
        counts = {c: colors.count(c) for c in used}
        victim = min(used, key=lambda c: counts[c])
        trial = colors[:]
        removed = True
        for v in [i for i, c in enumerate(trial) if c == victim]:
            options = [c for c in used if c != victim
                       and all(trial[u] != c for u in adj[v])]
            if not options:
                removed = False
                break
            trial[v] = options[0]
        if not removed:
            break
        colors = trial
    return len(set(colors)), colors


def measure(action, repeats: int = 3):
    """Медиана времени action() и результат последнего запуска."""
    times = []
    result = None
    for _ in range(repeats):
        started = time.perf_counter()
        result = action()
        times.append(time.perf_counter() - started)
    return statistics.median(times), result


def exact_experiment():
    """Рост времени точного метода с размерностью."""
    rows = []
    for n in EXACT_SIZES:
        adj = random_graph(n, DENSITY, SEED + n)
        t, (k, colors) = measure(lambda: exact_chromatic(adj), repeats=1)
        assert is_valid(adj, colors)
        rows.append({"n": n, "k": k, "t": t})
    return rows


def m4_experiment():
    """М4: среднее и максимальное отклонение эвристики от точного оптимума."""
    rows = []
    for n in M4_SIZES:
        devs, hits = [], 0
        for trial in range(M4_TRIALS):
            adj = random_graph(n, DENSITY, SEED * 1000 + n * 100 + trial)
            opt, _ = exact_chromatic(adj)
            k_greedy, colors = greedy_by_degree(adj)
            k_ls, colors_ls = recolor_local_search(adj, colors)
            assert is_valid(adj, colors_ls)
            devs.append((k_ls - opt) / opt * 100)
            hits += k_ls == opt
        rows.append({"n": n, "mean": statistics.mean(devs), "max": max(devs),
                     "hit": hits / M4_TRIALS * 100})
    return rows


def large_experiment():
    """Эвристики на графе из LARGE_N вершин."""
    adj = random_graph(LARGE_N, LARGE_DENSITY, SEED)
    t_g, (k_g, colors_g) = measure(lambda: greedy_by_degree(adj))
    t_ls, (k_ls, colors_ls) = measure(lambda: recolor_local_search(adj, colors_g))
    assert is_valid(adj, colors_g) and is_valid(adj, colors_ls)
    edges = sum(len(s) for s in adj) // 2
    return {"edges": edges, "k_greedy": k_g, "t_greedy": t_g,
            "k_ls": k_ls, "t_ls": t_ls}


def verify() -> None:
    """Проверки на известных графах."""
    triangle = [{1, 2}, {0, 2}, {0, 1}]
    assert exact_chromatic(triangle)[0] == 3
    path = [{1}, {0, 2}, {1, 3}, {2}]
    assert exact_chromatic(path)[0] == 2
    k, colors = greedy_by_degree(path)
    assert is_valid(path, colors) and k == 2


def save_chart(exact_rows) -> None:
    out_dir = os.path.dirname(os.path.abspath(__file__))
    ns = [r["n"] for r in exact_rows]
    ts = [r["t"] for r in exact_rows]
    plt.figure(figsize=(8, 5))
    plt.plot(ns, ts, "o-", label="Точный метод (перебор с отсечением)")
    plt.yscale("log")
    plt.xlabel("Число вершин n")
    plt.ylabel("Время, с (логарифмическая шкала)")
    plt.title(f"Рост времени точного метода раскраски, плотность {DENSITY}")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr12_exact.png"), dpi=160)
    plt.close()


def main() -> None:
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}\n")

    verify()
    print("Проверки на известных графах пройдены (треугольник — 3, путь — 2).\n")

    print(f"Точный метод: плотность {DENSITY}")
    exact_rows = exact_experiment()
    print(f"{'n':>4}{'хроматическое число':>21}{'время, с':>13}")
    for r in exact_rows:
        print(f"{r['n']:>4}{r['k']:>21}{r['t']:>13.4f}")

    print(f"\nМ4: отклонение эвристики (жадная + перекраска) от оптимума, {M4_TRIALS} графов на n")
    print(f"{'n':>4}{'среднее, %':>13}{'максимум, %':>13}{'совпало, %':>13}")
    for r in m4_experiment():
        print(f"{r['n']:>4}{r['mean']:>13.2f}{r['max']:>13.2f}{r['hit']:>13.1f}")

    print(f"\nБольшой граф: n = {LARGE_N}, плотность {LARGE_DENSITY}")
    big = large_experiment()
    print(f"  Рёбер: {big['edges']}")
    print(f"  Жадная по степеням:    цветов {big['k_greedy']}, время {big['t_greedy']:.5f} с")
    print(f"  + перекраска:          цветов {big['k_ls']}, время {big['t_ls']:.5f} с")

    save_chart(exact_rows)
    print("\nГрафик сохранён: lr12_exact.png")


if __name__ == "__main__":
    main()
