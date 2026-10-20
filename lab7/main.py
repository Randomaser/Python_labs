"""
Лабораторная работа № 7. Вариант 4.
Задача А: число способов подняться по лестнице с шагами 1, 2, 3 — три реализации
          (наивная рекурсия, мемоизация, итеративное ДП).
Задача Б: размен суммы S = 200 номиналами 1, 3, 7 методом динамического программирования
          с восстановлением набора монет.
Г4: зависимость времени ДП от суммы S при фиксированном числе номиналов.
"""

import os
import platform
import statistics
import sys
import time

import matplotlib.pyplot as plt
import numpy as np


STEPS = (1, 2, 3)
SIZES_A = list(range(10, 29, 2))          # n = 10, 12, ..., 28
NAIVE_LIMIT_SECONDS = 10.0                # ориентир из методички
REPEATS = 5

COINS = (1, 3, 7)
S_TARGET = 200
S_SWEEP = [2000, 4000, 8000, 16000, 32000]  # Г4: фиксированы номиналы, меняется S

calls = 0  # счётчик вызовов рекурсивных функций


def stairs_naive(n: int) -> int:
    """Наивная рекурсия: W(n) = W(n-1) + W(n-2) + W(n-3). Время растёт экспоненциально."""
    global calls
    calls += 1
    if n == 0:
        return 1
    if n < 0:
        return 0
    return sum(stairs_naive(n - s) for s in STEPS)


def stairs_memo(n: int, cache: dict | None = None) -> int:
    """Нисходящее ДП: каждая подзадача вычисляется один раз и кэшируется."""
    global calls
    calls += 1
    if cache is None:
        cache = {}
    if n == 0:
        return 1
    if n < 0:
        return 0
    if n in cache:
        return cache[n]
    cache[n] = sum(stairs_memo(n - s, cache) for s in STEPS)
    return cache[n]


def stairs_iter(n: int) -> int:
    """Восходящее ДП: таблица ways[i] заполняется по возрастанию i."""
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        ways[i] = sum(ways[i - s] for s in STEPS if i - s >= 0)
    return ways[n]


def coin_change_dp(coins: tuple, amount: int):
    """
    Размен суммы минимальным числом монет.
    D[s] = 1 + min(D[s - c]) по номиналам c <= s, D[0] = 0.
    Возвращает (число монет, отсортированный список монет) либо (-1, []).
    """
    inf = float("inf")
    best = [0] + [inf] * amount
    choice = [0] * (amount + 1)
    for s in range(1, amount + 1):
        for c in coins:
            if c <= s and best[s - c] + 1 < best[s]:
                best[s] = best[s - c] + 1
                choice[s] = c
    if best[amount] == inf:
        return -1, []
    # восстановление: идём от суммы, вычитая выбранный номинал
    result, s = [], amount
    while s > 0:
        result.append(choice[s])
        s -= choice[s]
    return best[amount], sorted(result, reverse=True)


def coin_enumerate(amount: int) -> int:
    """Независимая проверка перебором для номиналов (1, 3, 7): перебор количеств монет."""
    best = None
    for c7 in range(amount // 7 + 1):
        for c3 in range((amount - 7 * c7) // 3 + 1):
            c1 = amount - 7 * c7 - 3 * c3
            count = c1 + c3 + c7
            if best is None or count < best:
                best = count
    return best


def tree_mermaid(n: int) -> tuple[str, int]:
    """Строит дерево вызовов наивной рекурсии в формате Mermaid; возвращает (текст, число узлов)."""
    lines = ["flowchart TD"]
    counter = [0]

    def walk(k: int, parent: str | None = None) -> None:
        counter[0] += 1
        name = f"N{counter[0]}"
        if k == 0:
            label = "W(0) = 1"
        elif k < 0:
            label = f"W({k}) = 0"
        else:
            label = f"W({k})"
        lines.append(f'    {name}["{label}"]')
        if parent is not None:
            lines.append(f"    {parent} --> {name}")
        if k > 0:
            for s in STEPS:
                walk(k - s, name)

    walk(n)
    return "\n".join(lines), counter[0]


def measure(action, repeats: int = REPEATS):
    """Медиана времени action() по repeats запускам; возвращает (время, результат последнего запуска)."""
    times = []
    result = None
    for _ in range(repeats):
        started = time.perf_counter()
        result = action()
        times.append(time.perf_counter() - started)
    return statistics.median(times), result


def count_calls(func, n: int):
    """Запускает рекурсивную функцию и возвращает (результат, число вызовов)."""
    global calls
    calls = 0
    result = func(n)
    return result, calls


def experiment_stairs() -> list[dict]:
    """Задача А: три реализации для n из SIZES_A. Наивную версию прекращаем при превышении лимита."""
    rows = []
    naive_running = True
    for n in SIZES_A:
        row = {"n": n}
        if naive_running:
            t_naive, (value_naive, calls_naive) = measure(lambda: count_calls(stairs_naive, n), repeats=1)
            row.update(naive_time=t_naive, naive_calls=calls_naive)
            if t_naive > NAIVE_LIMIT_SECONDS:
                naive_running = False
        else:
            value_naive = None
            row.update(naive_time=None, naive_calls=None)

        t_memo, (value_memo, calls_memo) = measure(lambda: count_calls(stairs_memo, n))
        t_iter, value_iter = measure(lambda: stairs_iter(n))
        assert value_memo == value_iter
        if value_naive is not None:
            assert value_naive == value_iter
        row.update(memo_time=t_memo, memo_calls=calls_memo, iter_time=t_iter, value=value_iter)
        rows.append(row)
    return rows


def experiment_coins() -> list[dict]:
    """Задача Б и Г4: ДП для размена; время как функция S при фиксированных номиналах."""
    for s in range(1, 61):
        assert coin_change_dp(COINS, s)[0] == coin_enumerate(s), f"несовпадение при S={s}"
    count, coins = coin_change_dp(COINS, S_TARGET)
    assert sum(coins) == S_TARGET and len(coins) == count

    rows = []
    for s in S_SWEEP:
        elapsed, _ = measure(lambda: coin_change_dp(COINS, s))
        rows.append({"S": s, "time": elapsed})
    return rows, count, coins


def linear_fit(xs: list[int], ys: list[float]):
    """Линейная регрессия y = a x + b; возвращает (a, b, R^2)."""
    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    ss_res = float(((y - pred) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return float(slope), float(intercept), 1 - ss_res / ss_tot


def save_charts(stairs_rows: list[dict], sweep_rows: list[dict]) -> None:
    """Сохраняет графики: число вызовов и время (задача А) и линейность ДП (Г4)."""
    out_dir = os.path.dirname(os.path.abspath(__file__))

    ns = [r["n"] for r in stairs_rows if r["naive_calls"] is not None]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(ns, [r["naive_calls"] for r in stairs_rows if r["naive_calls"] is not None],
                 "o-", label="Наивная рекурсия")
    axes[0].plot([r["n"] for r in stairs_rows], [r["memo_calls"] for r in stairs_rows],
                 "s-", label="Мемоизация")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("n")
    axes[0].set_ylabel("Число вызовов (лог. шкала)")
    axes[0].set_title("Задача А: число вызовов")
    axes[0].grid(True, which="both", linestyle="--", alpha=0.5)
    axes[0].legend()

    axes[1].plot(ns, [r["naive_time"] for r in stairs_rows if r["naive_calls"] is not None],
                 "o-", label="Наивная рекурсия")
    axes[1].plot([r["n"] for r in stairs_rows], [r["memo_time"] for r in stairs_rows],
                 "s-", label="Мемоизация")
    axes[1].plot([r["n"] for r in stairs_rows], [r["iter_time"] for r in stairs_rows],
                 "^-", label="Итеративная")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("n")
    axes[1].set_ylabel("Время, с (лог. шкала)")
    axes[1].set_title("Задача А: время")
    axes[1].grid(True, which="both", linestyle="--", alpha=0.5)
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "lr7_stairs.png"), dpi=160)
    plt.close(fig)

    xs = [r["S"] for r in sweep_rows]
    ys = [r["time"] for r in sweep_rows]
    slope, intercept, _ = linear_fit(xs, ys)
    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, "o", label="Измерения ДП")
    plt.plot(xs, [slope * x + intercept for x in xs], "k--", label="Линейная аппроксимация")
    plt.xlabel("Сумма S")
    plt.ylabel("Время, с")
    plt.title("Г4: время ДП размена при номиналах 1, 3, 7")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr7_coins_sweep.png"), dpi=160)
    plt.close()


def main() -> None:
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}\n")

    tree_text, tree_nodes = tree_mermaid(3)
    out_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(out_dir, "lr7_tree.mmd"), "w", encoding="utf-8") as f:
        f.write(tree_text + "\n")
    print(f"Дерево рекурсии для n = 3: {tree_nodes} узлов (сохранено в lr7_tree.mmd)\n")

    print("Задача А: лестница с шагами 1, 2, 3")
    stairs_rows = experiment_stairs()
    print(f"{'n':>3} | {'наивная, с':>11} | {'вызовов':>11} | {'мемо, с':>10} | {'вызовов':>7} | "
          f"{'итер., с':>10} | {'ответ':>10}")
    print("-" * 85)
    for r in stairs_rows:
        naive_t = f"{r['naive_time']:.4f}" if r["naive_time"] is not None else "не изм."
        naive_c = str(r["naive_calls"]) if r["naive_calls"] is not None else "—"
        print(f"{r['n']:>3} | {naive_t:>11} | {naive_c:>11} | {r['memo_time']:>10.6f} | "
              f"{r['memo_calls']:>7} | {r['iter_time']:>10.6f} | {r['value']:>10}")

    print(f"\nЗадача Б: размен S = {S_TARGET}, номиналы {COINS}")
    sweep_rows_base, count, coins = experiment_coins()
    print(f"Минимум монет: {count}; набор: {coins}; проверка перебором для S = 1..60 пройдена")

    print("\nГ4: зависимость времени ДП от S (номиналы фиксированы)")
    print(f"{'S':>7} | {'время, с':>10}")
    print("-" * 22)
    for r in sweep_rows_base:
        print(f"{r['S']:>7} | {r['time']:>10.6f}")
    slope, intercept, r2 = linear_fit([r["S"] for r in sweep_rows_base], [r["time"] for r in sweep_rows_base])
    print(f"Линейная регрессия: T(S) ≈ {slope:.3e} * S + {intercept:.3e}, R² = {r2:.4f}")

    save_charts(stairs_rows, sweep_rows_base)
    print("\nГрафики сохранены: lr7_stairs.png, lr7_coins_sweep.png")


if __name__ == "__main__":
    main()
