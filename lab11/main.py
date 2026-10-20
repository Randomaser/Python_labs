"""
Лабораторная работа № 11. Вариант 4.
1. Поиск подстроки: наивный алгоритм и КМП на тексте с повторами и случайном тексте
   (образец «aaabaaa», n = 10^4, 10^5, 10^6, порог не применяется).
2. Л4: расстояние Левенштейна с памятью Θ(min(n, m)); сравнение с полной таблицей.
3. Сопоставление наименований контрагентов с порогом сходства 0,70.
"""

import os
import platform
import random
import re
import statistics
import sys
import time

import matplotlib.pyplot as plt


PATTERN = "aaabaaa"
PREFIX_EXPECTED = [0, 1, 2, 0, 1, 2, 3]   # ручной расчёт префикс-функции
SIZES = [10**4, 10**5, 10**6]
THRESHOLD = 0.70
REPEATS = 3
SEED = 42


def naive_search(text: str, pattern: str):
    """Наивный поиск. Возвращает (позиции, число сравнений символов)."""
    n, m = len(text), len(pattern)
    positions, comparisons = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            positions.append(i)
    return positions, comparisons


def prefix_function(pattern: str) -> list[int]:
    """π[i] — длина наибольшего собственного префикса P[0..i], совпадающего с его суффиксом."""
    pi = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_search(text: str, pattern: str):
    """Алгоритм Кнута — Морриса — Пратта. Θ(n + m). Возвращает (позиции, число сравнений)."""
    n, m = len(text), len(pattern)
    pi = prefix_function(pattern)
    positions, comparisons = [], 0
    k = 0
    for i in range(n):
        while k > 0 and text[i] != pattern[k]:
            comparisons += 1
            k = pi[k - 1]
        comparisons += 1
        if text[i] == pattern[k]:
            k += 1
        if k == m:
            positions.append(i - m + 1)
            k = pi[k - 1]
    return positions, comparisons


def levenshtein_full(a: str, b: str) -> int:
    """Полная таблица D[i][j]. Θ(nm) памяти (используется для сверки)."""
    n, m = len(a), len(b)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + cost)
    return D[n][m]


def levenshtein(a: str, b: str) -> int:
    """Л4: расстояние Левенштейна с двумя строками таблицы. Память Θ(min(n, m))."""
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            current.append(min(previous[j] + 1,
                               current[j - 1] + 1,
                               previous[j - 1] + (ca != cb)))
        previous = current
    return previous[-1]


def similarity(a: str, b: str) -> float:
    """Нормированная мера сходства из [0; 1]."""
    if not a and not b:
        return 1.0
    return 1 - levenshtein(a, b) / max(len(a), len(b))


LEGAL_FORMS = {"ооо", "оао", "зао", "пао", "ао", "ип"}


def normalize(name: str) -> str:
    """Нормализация наименования: регистр, ё→е, знаки, организационно-правовые формы."""
    s = name.lower().replace("ё", "е")
    s = re.sub(r"[\"'«»„“”.,()\-]", " ", s)
    words = [w for w in s.split() if w not in LEGAL_FORMS]
    return " ".join(words)


def match_records(list_a, list_b, threshold: float = THRESHOLD):
    """Сопоставление двух списков наименований: точное после нормализации, затем нечёткое."""
    norm_b = [(b, normalize(b)) for b in list_b]
    result = []
    for a in list_a:
        na = normalize(a)
        best, best_sim, kind = None, 0.0, ""
        for b, nb in norm_b:
            if na == nb:
                best, best_sim, kind = b, 1.0, "точное"
                break
            s = similarity(na, nb)
            if s > best_sim:
                best, best_sim, kind = b, s, "нечёткое"
        if best_sim >= threshold:
            result.append((a, best, best_sim, kind))
        else:
            result.append((a, None, best_sim, "не найдено"))
    return result


def measure(action, repeats: int = REPEATS):
    """Медиана времени action() и результат последнего запуска."""
    times = []
    result = None
    for _ in range(repeats):
        started = time.perf_counter()
        result = action()
        times.append(time.perf_counter() - started)
    return statistics.median(times), result


def search_experiment():
    """Сравнение наивного поиска и КМП на тексте с повторами и на случайном тексте."""
    rng = random.Random(SEED)
    rows = []
    for n in SIZES:
        random_text = "".join(rng.choice("abcd") for _ in range(n))
        repeat_text = "a" * n
        for label, text in (("случайный", random_text), ("с повторами", repeat_text)):
            t_naive, (pos_naive, c_naive) = measure(lambda: naive_search(text, PATTERN))
            t_kmp, (pos_kmp, c_kmp) = measure(lambda: kmp_search(text, PATTERN))
            assert pos_naive == pos_kmp
            rows.append({"n": n, "label": label, "t_naive": t_naive, "t_kmp": t_kmp,
                         "c_naive": c_naive, "c_kmp": c_kmp, "found": len(pos_kmp)})
    return rows


def levenshtein_experiment():
    """Л4: время и память-подобный показатель (размер таблицы) для полной таблицы и двух строк."""
    rng = random.Random(SEED + 1)
    rows = []
    for length in [200, 400, 800, 1600]:
        a = "".join(rng.choice("абвгд") for _ in range(length))
        b = "".join(rng.choice("абвгд") for _ in range(length))
        t_full, d_full = measure(lambda: levenshtein_full(a, b))
        t_rows, d_rows = measure(lambda: levenshtein(a, b))
        assert d_full == d_rows
        rows.append({"len": length, "t_full": t_full, "t_rows": t_rows,
                     "cells_full": (length + 1) ** 2, "cells_rows": 2 * (length + 1), "d": d_full})
    return rows


def verify() -> None:
    """Проверки корректности: префикс-функция, поиск, Левенштейн на известных примерах."""
    assert prefix_function(PATTERN) == PREFIX_EXPECTED
    assert levenshtein("кот", "скот") == 1
    assert levenshtein("Ромашка", "Ромашки") == 1
    text = "aaaabaaabaaaaaab"
    assert kmp_search(text, PATTERN)[0] == naive_search(text, PATTERN)[0]


def save_charts(search_rows, lev_rows) -> None:
    out_dir = os.path.dirname(os.path.abspath(__file__))
    repeat = [r for r in search_rows if r["label"] == "с повторами"]
    ns = [r["n"] for r in repeat]
    plt.figure(figsize=(8, 5))
    plt.plot(ns, [r["c_naive"] for r in repeat], "o-", label="Наивный, сравнения")
    plt.plot(ns, [r["c_kmp"] for r in repeat], "s-", label="КМП, сравнения")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Длина текста n (логарифмическая шкала)")
    plt.ylabel("Число сравнений символов (лог. шкала)")
    plt.title(f"Поиск подстроки «{PATTERN}» в тексте с повторами")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr11_search.png"), dpi=160)
    plt.close()

    lens = [r["len"] for r in lev_rows]
    plt.figure(figsize=(8, 5))
    plt.plot(lens, [r["t_full"] for r in lev_rows], "o-", label="Полная таблица, Θ(nm) памяти")
    plt.plot(lens, [r["t_rows"] for r in lev_rows], "s-", label="Две строки, Θ(min(n,m)) памяти")
    plt.xlabel("Длина строк n = m")
    plt.ylabel("Время, с")
    plt.title("Л4: расстояние Левенштейна")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "lr11_levenshtein.png"), dpi=160)
    plt.close()


def main() -> None:
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}\n")

    verify()
    print(f"π для «{PATTERN}»: {prefix_function(PATTERN)} (совпадает с ручным расчётом)\n")

    print("Поиск подстроки (медиана 3 запусков)")
    search_rows = search_experiment()
    print(f"{'n':>9}{'текст':>14}{'наивный, с':>13}{'КМП, с':>10}"
          f"{'сравн. наивн.':>16}{'сравн. КМП':>13}{'найдено':>9}")
    for r in search_rows:
        print(f"{r['n']:>9}{r['label']:>14}{r['t_naive']:>13.4f}{r['t_kmp']:>10.4f}"
              f"{r['c_naive']:>16}{r['c_kmp']:>13}{r['found']:>9}")

    print("\nЛ4: расстояние Левенштейна, полная таблица и две строки (медиана 3 запусков)")
    lev_rows = levenshtein_experiment()
    print(f"{'длина':>7}{'полная, с':>12}{'2 строки, с':>13}{'ячеек полн.':>14}{'ячеек 2 стр.':>14}{'d':>6}")
    for r in lev_rows:
        print(f"{r['len']:>7}{r['t_full']:>12.4f}{r['t_rows']:>13.4f}"
              f"{r['cells_full']:>14}{r['cells_rows']:>14}{r['d']:>6}")

    print(f"\nСопоставление контрагентов (порог {THRESHOLD})")
    system_a = ['ООО "Ромашка"', "АО Василёк", "ИП Иванов И.И.",
                'ООО "Северный ветер"', "ПАО Гранит"]
    system_b = ["Ромашка, ООО", "ВАСИЛЕК АО", "Иванов Иван Иванович",
                "Северный Ветер ООО", "Гранит-Строй ПАО"]
    for a, b, s, kind in match_records(system_a, system_b):
        target = b if b else "—"
        print(f"  {a:<24} → {target:<22} сходство {s:.3f} ({kind})")

    save_charts(search_rows, lev_rows)
    print("\nГрафики сохранены: lr11_search.png, lr11_levenshtein.png")


if __name__ == "__main__":
    main()
