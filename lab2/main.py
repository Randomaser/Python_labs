"""
Лабораторная работа № 2. Вариант 4 (согласовано с методическими указаниями).
Основное задание: Сравнение Bubble Sort и Insertion Sort на типах R при n in [200, 400, 800, 1600, 3200].
Дополнительное задание М4: Сравнение всех типов данных (R, S, V, N) при n = 3000 с построением столбчатой диаграммы.
"""

import random
import statistics
import time
import matplotlib.pyplot as plt


# ==========================================
# 1. Реализация алгоритмов сортировки
# ==========================================

def bubble_sort(arr: list) -> list:
    """
    Сортировка обменом ("пузырьком") с флагом досрочного выхода.
    Не меняет исходный массив, возвращает новый отсортированный список.
    """
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr: list) -> list:
    """
    Сортировка вставками.
    Не меняет исходный массив, возвращает новый отсортированный список.
    """
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# ==========================================
# 2. Вспомогательные функции (генерация и замер)
# ==========================================

def generate_data(n: int, kind: str = "R", lo: int = -500, hi: int = 500, seed: int = 42) -> list:
    """
    Генерирует массив длины n заданного типа:
    R - случайные, S - упорядоченные, V - обратно упорядоченные, N - почти упорядоченные.
    """
    rng = random.Random(seed + n)
    data = [rng.randint(lo, hi) for _ in range(n)]
    
    if kind == "S":
        data.sort()
    elif kind == "V":
        data.sort(reverse=True)
    elif kind == "N":
        data.sort()
        # 5% случайных перестановок пар
        for _ in range(max(1, n // 20)):
            i, j = rng.randrange(n), rng.randrange(n)
            data[i], data[j] = data[j], data[i]
            
    return data


def measure(sort_func, data: list, repeats: int = 5) -> float:
    """
    Возвращает медианное время работы sort_func на данных data (в секундах).
    """
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = sort_func(data)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        # Проверка корректности работы сортировки
        assert result == sorted(data), f"Ошибка в алгоритме {sort_func.__name__}"
    return statistics.median(times)


# ==========================================
# 3. Основной блок выполнения
# ==========================================

if __name__ == "__main__":
    # --- Основное задание (Вариант 4) ---
    SIZES = [200, 400, 800, 1600, 3200]
    REPEATS = 5
    algorithms = {"Пузырьком": bubble_sort, "Вставками": insertion_sort}
    results = {name: [] for name in algorithms}

    print("=== Основной эксперимент (Случайные данные R, диапазон [-500; 500]) ===")
    print(f"{'n':>6}" + "".join(f"{name:>16}" for name in algorithms))
    print("-" * 38)

    for n in SIZES:
        data = generate_data(n, kind="R", lo=-500, hi=500)
        row = f"{n:>6}"
        for name, func in algorithms.items():
            t = measure(func, data, REPEATS)
            results[name].append(t)
            row += f"{t:>16.6f}"
        print(row)

    # Построение графика зависимостей T(n)
    plt.figure(figsize=(8, 5))
    for name, times in results.items():
        plt.plot(SIZES, times, marker="o", label=name)
    plt.xlabel("Размер массива n")
    plt.ylabel("Время, с")
    plt.title("Вариант 4: Зависимость времени сортировки от n (Тип R)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("./lab2/lr2_main_plot.png", dpi=150)
    plt.close()

    # --- Дополнительное задание М4 ---
    print("\n=== Дополнительное задание М4 (n = 3000, все типы данных) ===")
    N_M4 = 3000
    DATA_TYPES = {"R": "Случайные", "S": "Упорядоченные", "V": "Обратно упор.", "N": "Почти упор."}
    m4_results = {alg_name: [] for alg_name in algorithms}

    print(f"{'Тип данных':<18}" + "".join(f"{name:>16}" for name in algorithms))
    print("-" * 50)

    for code, label in DATA_TYPES.items():
        data = generate_data(N_M4, kind=code, lo=-500, hi=500)
        row = f"{label:<18}"
        for name, func in algorithms.items():
            t = measure(func, data, REPEATS)
            m4_results[name].append(t)
            row += f"{t:>16.6f}"
        print(row)

    # Построение столбчатой диаграммы М4
    import numpy as np
    x = np.arange(len(DATA_TYPES))
    width = 0.35

    plt.figure(figsize=(9, 5))
    plt.bar(x - width/2, m4_results["Пузырьком"], width, label="Пузырьком")
    plt.bar(x + width/2, m4_results["Вставками"], width, label="Вставками")
    plt.xticks(x, list(DATA_TYPES.values()))
    plt.ylabel("Время, с")
    plt.title("Доп. задание М4: Сравнение алгоритмов на различных структурах данных (n = 3000)")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("./lab2/lr2_m4_bar.png", dpi=150)
    plt.close()

    print("\nГрафики lr2_main_plot.png и lr2_m4_bar.png успешно сохранены.")