"""Лабораторная работа № 4. Вариант 4, дополнительное задание Б4."""

import os
import platform
import random
import statistics
import sys
import time

import matplotlib.pyplot as plt


SIZES = [1_000, 5_000, 10_000, 100_000]
QUERY_COUNT = 1_000
REPEATS = 3
START_VALUE = 7
STEP = 3


def linear_search(values: list[int], query: int) -> tuple[int, int]:
    """Ищет ключ без требования к порядку; возвращает индекс и сравнения."""
    comparisons = 0
    for index, value in enumerate(values):
        comparisons += 1
        if value == query:
            return index, comparisons
    return -1, comparisons


def binary_search(values: list[int], query: int) -> tuple[int, int]:
    """Ищет ключ в отсортированном массиве."""
    left, right = 0, len(values) - 1
    comparisons = 0
    while left <= right:
        middle = left + (right - left) // 2
        comparisons += 1
        if values[middle] == query:
            return middle, comparisons
        comparisons += 1
        if values[middle] < query:
            left = middle + 1
        else:
            right = middle - 1
    return -1, comparisons


def interpolation_search(values: list[int], query: int) -> tuple[int, int]:
    """Ищет ключ в отсортированном массиве по оценке его позиции."""
    left, right = 0, len(values) - 1
    comparisons = 0
    while left <= right:
        comparisons += 1
        if query < values[left]:
            return -1, comparisons
        comparisons += 1
        if query > values[right]:
            return -1, comparisons
        if values[left] == values[right]:
            comparisons += 1
            return (left, comparisons) if values[left] == query else (-1, comparisons)
        position = left + (query - values[left]) * (right - left) // (
            values[right] - values[left]
        )
        comparisons += 1
        if values[position] == query:
            return position, comparisons
        comparisons += 1
        if values[position] < query:
            left = position + 1
        else:
            right = position - 1
    return -1, comparisons


def lower_bound(values: list[int], query: int) -> tuple[int, int]:
    """Возвращает позицию первого элемента, не меньшего query, и сравнения."""
    left, right = 0, len(values)
    comparisons = 0
    while left < right:
        middle = left + (right - left) // 2
        comparisons += 1
        if values[middle] < query:
            left = middle + 1
        else:
            right = middle
    return left, comparisons


def upper_bound(values: list[int], query: int) -> tuple[int, int]:
    """Возвращает позицию первого элемента, большего query, и сравнения."""
    left, right = 0, len(values)
    comparisons = 0
    while left < right:
        middle = left + (right - left) // 2
        comparisons += 1
        if values[middle] <= query:
            left = middle + 1
        else:
            right = middle
    return left, comparisons


def search_range(values: list[int], query: int) -> tuple[int, int, int, int]:
    """Возвращает первое/последнее вхождение, количество и сравнения."""
    first, first_comparisons = lower_bound(values, query)
    if first == len(values):
        return -1, -1, 0, first_comparisons
    first_comparisons += 1
    if values[first] != query:
        return -1, -1, 0, first_comparisons
    after_last, last_comparisons = upper_bound(values, query)
    last = after_last - 1
    return first, last, after_last - first, first_comparisons + last_comparisons


def make_progression(size: int) -> list[int]:
    """Создаёт вариант А: A[i] = c + d*i."""
    return [START_VALUE + STEP * index for index in range(size)]


def make_queries(values: list[int], count: int, seed: int) -> list[int]:
    """Выбирает успешные запросы с равномерным выбором индекса."""
    generator = random.Random(seed)
    return [values[generator.randrange(len(values))] for _ in range(count)]


def benchmark(search, values: list[int], queries: list[int]) -> tuple[float, float]:
    """Возвращает медиану времени на запрос и среднее число сравнений."""
    durations = []
    comparison_totals = []
    for _ in range(REPEATS):
        total_comparisons = 0
        started = time.perf_counter()
        for query in queries:
            _, comparisons = search(values, query)
            total_comparisons += comparisons
        durations.append((time.perf_counter() - started) / len(queries))
        comparison_totals.append(total_comparisons / len(queries))
    for query in queries:
        index, _ = search(values, query)
        assert index >= 0 and values[index] == query
    return statistics.median(durations), statistics.mean(comparison_totals)


def benchmark_break_even(values: list[int], queries: list[int]) -> list[tuple[int, float, float]]:
    """Сравнивает линейный поиск и сортировку с последующими двоичными запросами."""
    unsorted_values = values.copy()
    random.Random(len(values)).shuffle(unsorted_values)
    query_counts = [1, 5, 10, 20, 50, 100, 200, 500, QUERY_COUNT]
    results = []
    sort_durations = []
    sorted_values = sorted(unsorted_values)
    for _ in range(REPEATS):
        started = time.perf_counter()
        sorted(unsorted_values)
        sort_durations.append(time.perf_counter() - started)
    sort_time = statistics.median(sort_durations)

    for count in query_counts:
        selected_queries = queries[:count]
        linear_durations = []
        binary_durations = []
        for _ in range(REPEATS):
            started = time.perf_counter()
            for query in selected_queries:
                linear_search(unsorted_values, query)
            linear_durations.append(time.perf_counter() - started)

            started = time.perf_counter()
            for query in selected_queries:
                binary_search(sorted_values, query)
            binary_durations.append(time.perf_counter() - started)
        for query in selected_queries:
            linear_index, _ = linear_search(unsorted_values, query)
            binary_index, _ = binary_search(sorted_values, query)
            assert linear_index >= 0 and unsorted_values[linear_index] == query
            assert binary_index >= 0 and sorted_values[binary_index] == query
        sorted_strategy_time = sort_time + statistics.median(binary_durations)
        results.append((count, statistics.median(linear_durations), sorted_strategy_time))
    return results


def compare_distributions(size: int = 10_000) -> list[tuple[str, float, float]]:
    """Сравнивает интерполяционный поиск на прогрессии и степенных ключах."""
    generator = random.Random(404)
    uniform_values = make_progression(size)
    skewed_sample = [int(1_000_000 * generator.random() ** 3) for _ in range(size)]
    skewed_values = sorted(set(skewed_sample))
    rows = []
    for label, values in (("Арифметическая прогрессия", uniform_values), ("Степенное распределение", skewed_values)):
        queries = (
            make_queries(values, QUERY_COUNT, 405)
            if label == "Арифметическая прогрессия"
            else [generator.choice(skewed_sample) for _ in range(QUERY_COUNT)]
        )
        elapsed, comparisons = benchmark(interpolation_search, values, queries)
        rows.append((label, elapsed, comparisons))
    return rows


def save_charts(sizes: list[int], timings: dict[str, list[float]], comparisons: dict[str, list[float]], break_even: list[tuple[int, float, float]]) -> None:
    """Сохраняет графики времени, сравнений и окупаемости сортировки."""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    for filename, series, ylabel, title in (
        ("lr4_time.png", timings, "Время одного запроса, с", "Время поиска, вариант 4"),
        ("lr4_comparisons.png", comparisons, "Сравнений на запрос", "Сравнения ключа, вариант 4"),
    ):
        plt.figure(figsize=(8, 5))
        for name, values in series.items():
            plt.plot(sizes, values, marker="o", label=name)
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Размер массива n (логарифмическая шкала)")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True, which="both", linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, filename), dpi=160)
        plt.close()

    query_counts = [row[0] for row in break_even]
    plt.figure(figsize=(8, 5))
    plt.plot(query_counts, [row[1] for row in break_even], marker="o", label="Без сортировки: линейный поиск")
    plt.plot(query_counts, [row[2] for row in break_even], marker="o", label="Сортировка + двоичный поиск")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Число запросов k (логарифмическая шкала)")
    plt.ylabel("Суммарное время, с")
    plt.title("Окупаемость предварительной сортировки, n = 100 000")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "lr4_breakeven.png"), dpi=160)
    plt.close()


def main() -> None:
    algorithms = {
        "Последовательный": linear_search,
        "Двоичный": binary_search,
        "Интерполяционный": interpolation_search,
    }
    timings = {name: [] for name in algorithms}
    comparisons = {name: [] for name in algorithms}

    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; CPU: {platform.processor()}; логических процессоров: {os.cpu_count()}")
    print("Вариант 4: A[i] = c + d*i, c = 7, d = 3; 1000 успешных запросов")
    print("\nСреднее время одного запроса и сравнения")
    print(f"{'n':>9} | {'Алгоритм':<20} | {'мкс/запрос':>12} | {'сравнений':>12}")
    print("-" * 66)

    for size in SIZES:
        values = make_progression(size)
        queries = make_queries(values, QUERY_COUNT, 100 + size)
        for name, search in algorithms.items():
            elapsed, average_comparisons = benchmark(search, values, queries)
            timings[name].append(elapsed)
            comparisons[name].append(average_comparisons)
            print(f"{size:>9} | {name:<20} | {elapsed * 1e6:>12.3f} | {average_comparisons:>12.2f}")

    print("\nБ4: поиск диапазона повторяющегося ключа")
    duplicate_values = [1, 2, 2, 2, 4, 7, 7, 9]
    first, last, count, range_comparisons = search_range(duplicate_values, 2)
    assert (first, last, count) == (1, 3, 3)
    print(f"A = {duplicate_values}, q = 2: первое = {first}, последнее = {last}, количество = {count}, сравнений = {range_comparisons}")
    print(f"Несуществующий ключ q = 3: {search_range(duplicate_values, 3)}")

    largest_values = make_progression(SIZES[-1])
    largest_queries = make_queries(largest_values, QUERY_COUNT, 100 + SIZES[-1])
    break_even = benchmark_break_even(largest_values, largest_queries)
    print("\nОкупаемость сортировки для n = 100 000")
    print(f"{'k':>7} | {'без сортировки, с':>20} | {'сортировка + поиск, с':>24}")
    print("-" * 58)
    for count, linear_time, sorted_time in break_even:
        print(f"{count:>7} | {linear_time:>20.6f} | {sorted_time:>24.6f}")

    print("\nИнтерполяционный поиск для разных распределений, n = 10 000")
    for label, elapsed, average_comparisons in compare_distributions():
        print(f"{label}: {elapsed * 1e6:.3f} мкс/запрос, {average_comparisons:.2f} сравнений")

    save_charts(SIZES, timings, comparisons, break_even)
    print("\nГрафики сохранены: lr4_time.png, lr4_comparisons.png, lr4_breakeven.png")


if __name__ == "__main__":
    main()