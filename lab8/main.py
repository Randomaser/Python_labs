"""
Лабораторная работа № 8. Вариант 4.
Размен суммы номиналами 1, 6, 9 (S <= 150): два жадных критерия
(наибольший номинал, наименьший номинал) против точного решения методом ДП.
Ж4: зависимость среднего отклонения жадного решения от размерности задачи.
Размерность для размена суммы понимается как верхняя граница суммы S_max.
"""

import os
import platform
import random
import statistics
import sys
import time

import matplotlib.pyplot as plt


COINS = (1, 6, 9)
S_MAX = 150
TRIALS = 500
SEED = 2024
DIMENSIONS = [5, 10, 20, 40, 80]   # Ж4: размерность S_max
DIM_TRIALS = 300
TIMING_SUMS = [1000, 5000, 20000, 50000]


def coin_dp(coins, amount):
    """Точное решение ДП: возвращает (минимум монет, отсортированный набор)."""
    inf = float("inf")
    best = [0] + [inf] * amount
    choice = [0] * (amount + 1)
    for s in range(1, amount + 1):
        for c in coins:
            if c <= s and best[s - c] + 1 < best[s]:
                best[s] = best[s - c] + 1
                choice[s] = c
    result, s = [], amount
    while s > 0:
        result.append(choice[s])
        s -= choice[s]
    return int(best[amount]), sorted(result, reverse=True)


def greedy_coins(coins, amount, largest_first=True):
    """Жадный размен: номиналы обходятся в заданном порядке, каждый берётся максимально возможное число раз."""
    order = sorted(coins, reverse=largest_first)
    remain, chosen = amount, []
    for c in order:
        k = remain // c
        chosen += [c] * k
        remain -= k * c
    assert remain == 0, "система номиналов должна содержать 1"
    return len(chosen), sorted(chosen, reverse=True)


def greedy_count(coins, amount, largest_first=True):
    """Только число монет жадного размена без построения списка (для замера времени)."""
    order = sorted(coins, reverse=largest_first)
    remain, count = amount, 0
    for c in order:
        k = remain // c
        count += k
        remain -= k * c
    return count


def deviation(greedy: int, optimum: int) -> float:
    """Относительное отклонение жадного решения от оптимума, %."""
    return (greedy - optimum) / optimum * 100


def random_sums(seed: int, count: int, s_max: int) -> list[int]:
    """Случайные суммы S из [1; s_max]."""
    rng = random.Random(seed)
    return [rng.randint(1, s_max) for _ in range(count)]


def experiment():
    """Серия из TRIALS случайных сумм: отклонения и доля точных совпадений."""
    sums = random_sums(SEED, TRIALS, S_MAX)
    criteria = {"Наибольший номинал": True, "Наименьший номинал": False}
    dev = {name: [] for name in criteria}
    hits = {name: 0 for name in criteria}
    for s in sums:
        opt, _ = coin_dp(COINS, s)
        for name, largest in criteria.items():
            g, _ = greedy_coins(COINS, s, largest)
            dev[name].append(deviation(g, opt))
            if g == opt:
                hits[name] += 1
    return dev, hits


def dimension_experiment():
    """Ж4: среднее и максимальное отклонение жадного критерия «наибольший номинал» при разных S_max."""
    rows = []
    for s_max in DIMENSIONS:
        sums = random_sums(SEED + s_max, DIM_TRIALS, s_max)
        devs = []
        for s in sums:
            opt, _ = coin_dp(COINS, s)
            g, _ = greedy_coins(COINS, s, True)
            devs.append(deviation(g, opt))
        rows.append((s_max, statistics.mean(devs), max(devs)))
    return rows


def timing_experiment():
    """Время жадного алгоритма и ДП при росте суммы S (номиналы фиксированы)."""
    rows = []
    for s in TIMING_SUMS:
        started = time.perf_counter()
        greedy_count(COINS, s, True)
        t_greedy = time.perf_counter() - started
        started = time.perf_counter()
        coin_dp(COINS, s)
        t_dp = time.perf_counter() - started
        rows.append((s, t_greedy, t_dp))
    return rows


def save_charts(dim_rows, timing_rows):
    """Сохраняет график зависимости отклонения от размерности и график времени."""
    out_dir = os.path.dirname(os.path.abspath(__file__))

    xs = [r[0] for r in dim_rows]
    plt.figure(figsize=(8, 5))
    plt.plot(xs, [r[1] for r in dim_rows], "o-", label="Среднее отклонение")
    plt.plot(xs, [r[2] for r in dim_rows], "s--", label="Максимальное отклонение")
    plt.xscale("log")
    plt.xlabel("Размерность S_max (логарифмическая шкала)")
    plt.ylabel("Отклонение от оптимума, %")
    plt.title("Ж4: жадный критерий «наибольший номинал», номиналы 1, 6, 9")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr8_dimension.png"), dpi=160)
    plt.close()

    ss = [r[0] for r in timing_rows]
    plt.figure(figsize=(8, 5))
    plt.plot(ss, [r[1] for r in timing_rows], "o-", label="Жадный (O(k))")
    plt.plot(ss, [r[2] for r in timing_rows], "s-", label="ДП (Θ(kS))")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Сумма S (логарифмическая шкала)")
    plt.ylabel("Время, с (логарифмическая шкала)")
    plt.title("Время жадного алгоритма и ДП при номиналах 1, 6, 9")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr8_timing.png"), dpi=160)
    plt.close()


def main():
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}\n")

    print(f"Контрпример: номиналы {COINS}, S = 12")
    g_big, chosen_big = greedy_coins(COINS, 12, True)
    g_small, chosen_small = greedy_coins(COINS, 12, False)
    opt, chosen_opt = coin_dp(COINS, 12)
    print(f"  Наибольший номинал: {chosen_big}, монет {g_big}, отклонение {deviation(g_big, opt):.1f} %")
    print(f"  Наименьший номинал: {chosen_small}, монет {g_small}, отклонение {deviation(g_small, opt):.1f} %")
    print(f"  Оптимум (ДП): {chosen_opt}, монет {opt}\n")

    dev, hits = experiment()
    print(f"Серия из {TRIALS} случайных сумм S из [1; {S_MAX}]:")
    print(f"{'Критерий':<22}{'среднее, %':>12}{'медиана, %':>12}{'максимум, %':>13}{'совпало, %':>12}")
    for name, d in dev.items():
        print(f"{name:<22}{statistics.mean(d):>12.2f}{statistics.median(d):>12.2f}"
              f"{max(d):>13.2f}{hits[name] / TRIALS * 100:>12.1f}")

    print(f"\nЖ4: зависимость отклонения (наибольший номинал) от размерности S_max, {DIM_TRIALS} сумм на точку")
    print(f"{'S_max':>7}{'среднее, %':>13}{'максимум, %':>13}")
    dim_rows = dimension_experiment()
    for s_max, mean_dev, max_dev in dim_rows:
        print(f"{s_max:>7}{mean_dev:>13.2f}{max_dev:>13.2f}")

    print("\nСравнение времени")
    timing_rows = timing_experiment()
    print(f"{'S':>7}{'жадный, с':>14}{'ДП, с':>12}{'отношение':>12}")
    for s, t_g, t_dp in timing_rows:
        print(f"{s:>7}{t_g:>14.6f}{t_dp:>12.4f}{t_dp / t_g:>12.1f}")

    save_charts(dim_rows, timing_rows)
    print("\nГрафики сохранены: lr8_dimension.png, lr8_timing.png")


if __name__ == "__main__":
    main()
