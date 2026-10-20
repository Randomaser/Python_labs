"""
Лабораторная работа № 5. Вариант 4.
Хеш-таблица с открытой адресацией: линейное и квадратичное пробирование,
метод деления h(k) = k mod m (m — простое число).
Дополнительное задание В4: зависимость числа проб от коэффициента заполнения α.
"""

import math
import os
import platform
import random
import statistics
import sys
import time

import matplotlib.pyplot as plt


M = 65_521            # размер таблицы (простое число)
N = 40_000            # число ключей варианта 4
QUERY_COUNT = 10_000  # число запросов каждого типа
REPEATS = 3           # повторы замеров, берётся медиана
ALPHAS = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95]
KEY_RANGE = 10_000_000
METHOD_NAMES = {"linear": "Линейное", "quadratic": "Квадратичное"}


class OpenAddressingTable:
    """Хеш-таблица с открытой адресацией. method: 'linear' или 'quadratic'."""

    def __init__(self, m: int = M, method: str = "linear"):
        if method not in METHOD_NAMES:
            raise ValueError("Неизвестный способ пробирования")
        self.m = m
        self.method = method
        self.slots = [None] * m
        self.n = 0

    def _h(self, key: int) -> int:
        """Метод деления: h(k) = k mod m."""
        return key % self.m

    def probe_sequence(self, key: int):
        """Генерирует позиции проб для ключа."""
        base = self._h(key)
        if self.method == "linear":
            for i in range(self.m):
                yield (base + i) % self.m
            return
        # Квадратичная фаза: слагаемые T_i = i(i+1)/2 при i < (m+1)/2
        # различны по модулю простого m, то есть дают (m+1)/2 разных позиций.
        for i in range((self.m + 1) // 2):
            yield (base + i * (i + 1) // 2) % self.m
        # Линейный резерв: квадратичная фаза не покрывает все ячейки простого m,
        # поэтому после неё проверяются все ячейки подряд, чтобы вставка не терялась.
        for i in range(self.m):
            yield (base + i) % self.m

    def insert(self, key: int) -> int:
        """Вставляет ключ и возвращает число проб."""
        probes = 0
        for pos in self.probe_sequence(key):
            probes += 1
            stored = self.slots[pos]
            if stored is None:
                self.slots[pos] = key
                self.n += 1
                return probes
            if stored == key:
                return probes
        raise RuntimeError("Таблица переполнена")

    def search(self, key: int) -> tuple[bool, int]:
        """Ищет ключ; возвращает (найден ли он, число проб)."""
        probes = 0
        for pos in self.probe_sequence(key):
            probes += 1
            stored = self.slots[pos]
            if stored is None:
                return False, probes
            if stored == key:
                return True, probes
        return False, probes


def make_keys(count: int, seed: int) -> list[int]:
    """Уникальные случайные целые ключи из диапазона [0; KEY_RANGE)."""
    return random.Random(seed).sample(range(KEY_RANGE), count)


def missing_keys(count: int, seed: int) -> list[int]:
    """Ключи из диапазона, который не пересекается с хранимыми ключами."""
    rng = random.Random(seed)
    return [rng.randrange(KEY_RANGE, 2 * KEY_RANGE) for _ in range(count)]


def build_table(method: str, keys: list[int]):
    """Вставляет ключи; возвращает таблицу, время вставки и среднее число проб."""
    table = OpenAddressingTable(M, method)
    insert_probes = 0
    started = time.perf_counter()
    for key in keys:
        insert_probes += table.insert(key)
    elapsed = time.perf_counter() - started
    return table, elapsed, insert_probes / len(keys)


def search_stats(table: OpenAddressingTable, queries: list[int]) -> tuple[float, float]:
    """Возвращает медиану времени на запрос (с) и среднее число проб."""
    durations = []
    probes = 0.0
    for _ in range(REPEATS):
        total = 0
        started = time.perf_counter()
        for query in queries:
            _, query_probes = table.search(query)
            total += query_probes
        durations.append((time.perf_counter() - started) / len(queries))
        probes = total / len(queries)
    return statistics.median(durations), probes


def probes_only(table: OpenAddressingTable, queries: list[int]) -> float:
    """Среднее число проб без замера времени."""
    return sum(table.search(query)[1] for query in queries) / len(queries)


def verify(table: OpenAddressingTable, present: list[int], absent: list[int]) -> None:
    """Проверяет корректность: хранимые ключи находятся, отсутствующие — нет."""
    assert all(table.search(key)[0] for key in present)
    assert not any(table.search(key)[0] for key in absent)


def main_experiment() -> list[dict]:
    """Основное задание варианта 4: линейное и квадратичное пробирование."""
    keys = make_keys(N, seed=42)
    successful = random.Random(43).choices(keys, k=QUERY_COUNT)
    unsuccessful = missing_keys(QUERY_COUNT, seed=44)
    rows = []
    for method in ("linear", "quadratic"):
        insert_times = []
        for _ in range(REPEATS):
            table, elapsed, insert_probes = build_table(method, keys)
            insert_times.append(elapsed)
        verify(table, successful, unsuccessful)
        succ_time, succ_probes = search_stats(table, successful)
        unsucc_time, unsucc_probes = search_stats(table, unsuccessful)
        rows.append({
            "method": method,
            "insert_time": statistics.median(insert_times),
            "insert_probes": insert_probes,
            "succ_time": succ_time,
            "succ_probes": succ_probes,
            "unsucc_time": unsucc_time,
            "unsucc_probes": unsucc_probes,
        })
    return rows


def alpha_experiment() -> list[dict]:
    """Дополнительное задание В4: число проб в зависимости от α."""
    rng = random.Random(77)
    rows = []
    for alpha in ALPHAS:
        n = round(alpha * M)
        keys = rng.sample(range(KEY_RANGE), n)
        successful = rng.choices(keys, k=QUERY_COUNT)
        unsuccessful = [rng.randrange(KEY_RANGE, 2 * KEY_RANGE) for _ in range(QUERY_COUNT)]
        row = {"alpha": alpha, "n": n}
        for method in ("linear", "quadratic"):
            table, _, _ = build_table(method, keys)
            verify(table, successful, unsuccessful)
            row[f"{method}_succ"] = probes_only(table, successful)
            row[f"{method}_unsucc"] = probes_only(table, unsuccessful)
        rows.append(row)
    return rows


def save_charts(main_rows: list[dict], alpha_rows: list[dict]) -> None:
    """Сохраняет график В4 и столбчатую диаграмму основного задания."""
    out_dir = os.path.dirname(os.path.abspath(__file__))
    alphas = [row["alpha"] for row in alpha_rows]

    plt.figure(figsize=(9, 6))
    plt.plot(alphas, [r["linear_unsucc"] for r in alpha_rows], "o-", label="Линейное, неуспешный")
    plt.plot(alphas, [r["linear_succ"] for r in alpha_rows], "s-", label="Линейное, успешный")
    plt.plot(alphas, [r["quadratic_unsucc"] for r in alpha_rows], "^-", label="Квадратичное, неуспешный")
    plt.plot(alphas, [r["quadratic_succ"] for r in alpha_rows], "v-", label="Квадратичное, успешный")
    grid = [i / 1000 for i in range(1, 951)]
    plt.plot(grid, [1 / (1 - a) for a in grid], "k--", label="Теория 1/(1-α)")
    plt.plot(grid, [math.log(1 / (1 - a)) / a for a in grid], "k:", label="Теория успешного поиска")
    plt.yscale("log")
    plt.xlabel("Коэффициент заполнения α")
    plt.ylabel("Среднее число проб (логарифмическая шкала)")
    plt.title("В4: число проб в зависимости от α, m = 65 521")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr5_alpha.png"), dpi=160)
    plt.close()

    linear, quadratic = main_rows
    x = [0, 1]
    width = 0.35
    plt.figure(figsize=(8, 5))
    plt.bar([i - width / 2 for i in x], [linear["succ_probes"], linear["unsucc_probes"]], width, label="Линейное")
    plt.bar([i + width / 2 for i in x], [quadratic["succ_probes"], quadratic["unsucc_probes"]], width, label="Квадратичное")
    plt.xticks(x, ["Успешный поиск", "Неуспешный поиск"])
    plt.ylabel("Среднее число проб")
    plt.title("Основное задание: n = 40 000, m = 65 521, α ≈ 0,61")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr5_main_probes.png"), dpi=160)
    plt.close()


def main() -> None:
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}")
    print(f"Вариант 4: целые случайные ключи, метод деления, m = {M}, n = {N}, α = {N / M:.3f}\n")

    main_rows = main_experiment()
    print(f"{'Пробирование':<14} | {'вставка, с':>11} | {'проб/вставку':>12} | {'успеш., мкс':>11} | "
          f"{'проб':>7} | {'неуспеш., мкс':>13} | {'проб':>7}")
    print("-" * 94)
    for row in main_rows:
        print(f"{METHOD_NAMES[row['method']]:<14} | {row['insert_time']:>11.4f} | {row['insert_probes']:>12.2f} | "
              f"{row['succ_time'] * 1e6:>11.3f} | {row['succ_probes']:>7.2f} | "
              f"{row['unsucc_time'] * 1e6:>13.3f} | {row['unsucc_probes']:>7.2f}")

    print("\nВ4: зависимость числа проб от α")
    alpha_rows = alpha_experiment()
    print(f"{'α':>5} | {'n':>6} | {'лин. успеш.':>11} | {'лин. неуспеш.':>13} | "
          f"{'квадр. успеш.':>13} | {'квадр. неуспеш.':>15} | {'1/(1-α)':>8}")
    print("-" * 96)
    for row in alpha_rows:
        print(f"{row['alpha']:>5.2f} | {row['n']:>6} | {row['linear_succ']:>11.2f} | "
              f"{row['linear_unsucc']:>13.2f} | {row['quadratic_succ']:>13.2f} | "
              f"{row['quadratic_unsucc']:>15.2f} | {1 / (1 - row['alpha']):>8.2f}")

    save_charts(main_rows, alpha_rows)
    print("\nГрафики сохранены: lr5_alpha.png, lr5_main_probes.png")


if __name__ == "__main__":
    main()
