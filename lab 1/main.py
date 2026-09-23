"""
Лабораторная работа № 1. Вариант 4.
Вычисление √a, ∛b и ln(c) итерационными методами.
Дополнительное требование Д3: Нормализация аргумента логарифма.
"""

import math

# Константы варианта 4
A_VAL = 0.25
B_VAL = 15.0
C_VAL = 10.0
EPS = 1e-4
N_MAX = 1000


def sqrt_newton_residual(a: float, eps: float = EPS, n_max: int = N_MAX):
    """
    Вычисление √a методом Ньютона.
    Критерий остановки: по невязке |x^2 - a| < eps.
    Начальное приближение: x0 = 1.
    """
    if a < 0:
        raise ValueError("Подкоренное выражение должно быть неотрицательным.")
    if a == 0:
        return 0.0, 0

    x = 1.0  # Условие варианта 4: x0 = 1
    for n in range(1, n_max + 1):
        x_new = 0.5 * (x + a / x)
        # Проверка критерия невязки
        if abs(x_new**2 - a) < eps:
            return x_new, n
        x = x_new
    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def cbrt_newton_residual(b: float, eps: float = EPS, n_max: int = N_MAX):
    """
    Вычисление ∛b методом Ньютона.
    Критерий остановки: по невязке |x^3 - b| < eps.
    Начальное приближение: x0 = 1.
    """
    if b == 0:
        return 0.0, 0

    sign = -1.0 if b < 0 else 1.0
    abs_b = abs(b)
    x = 1.0  # Условие варианта 4: x0 = 1

    for n in range(1, n_max + 1):
        x_new = (2.0 * x + abs_b / (x * x)) / 3.0
        # Проверка критерия невязки
        if abs(x_new**3 - abs_b) < eps:
            return sign * x_new, n
        x = x_new
    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def ln_series_basic(c: float, eps: float = EPS, n_max: int = 10_000):
    """
    Вычисление ln(c) базовым методом ряда без нормализации.
    """
    if c <= 0:
        raise ValueError("Аргумент логарифма должен быть больше 0.")

    y = (c - 1.0) / (c + 1.0)
    y2 = y * y
    power = y
    total = 0.0

    for k in range(n_max):
        term = 2.0 * power / (2 * k + 1)
        if abs(term) < eps:
            return total, k
        total += term
        power *= y2

    raise RuntimeError("Точность не достигнута за N_MAX итераций")


def ln_series_normalized(c: float, eps: float = EPS):
    """
    Требование Д3: Вычисление ln(c) с нормализацией аргумента c = m * 2^k, m ∈ [0.5, 1).
    ln(c) = ln(m) + k * ln(2).
    """
    if c <= 0:
        raise ValueError("Аргумент логарифма должен быть больше 0.")

    # 1. Приведение к форме c = m * 2^k
    # frexp возвращает (m, k), где m ∈ [0.5, 1)
    m, k = math.frexp(c)

    # 2. Вычисление ln(m)
    val_m, iters_m = ln_series_basic(m, eps)

    # 3. Вычисление константы ln(2)
    val_ln2, iters_ln2 = ln_series_basic(2.0, eps)

    # Итоговый результат и суммарное число итераций
    total_ln = val_m + k * val_ln2
    total_iters = iters_m + iters_ln2

    return total_ln, total_iters


if __name__ == "__main__":
    # 1. Вычисление основных функций варианта 4
    val_sqrt, iter_sqrt = sqrt_newton_residual(A_VAL)
    val_cbrt, iter_cbrt = cbrt_newton_residual(B_VAL)
    val_ln, iter_ln_base = ln_series_basic(C_VAL)

    # 2. Выполнение требования Д3
    val_ln_norm, iter_ln_norm = ln_series_normalized(C_VAL)

    # 3. Вывод сводной таблицы результатов
    print("=" * 85)
    print(f"{'Функция':<12}{'Аргумент':>10}{'Результат':>16}{'Эталон (math)':>16}{'Погрешность':>14}{'Итерации':>10}")
    print("-" * 85)

    ref_sqrt = math.sqrt(A_VAL)
    print(f"{'sqrt(a)':<12}{A_VAL:>10.2f}{val_sqrt:>16.8f}{ref_sqrt:>16.8f}{abs(val_sqrt - ref_sqrt):>14.2e}{iter_sqrt:>10}")

    ref_cbrt = B_VAL ** (1/3)
    print(f"{'cbrt(b)':<12}{B_VAL:>10.2f}{val_cbrt:>16.8f}{ref_cbrt:>16.8f}{abs(val_cbrt - ref_cbrt):>14.2e}{iter_cbrt:>10}")

    ref_ln = math.log(C_VAL)
    print(f"{'ln(c) базовый':<10}{C_VAL:>10.2f}{val_ln:>16.8f}{ref_ln:>16.8f}{abs(val_ln - ref_ln):>14.2e}{iter_ln_base:>10}")
    print(f"{'ln(c) норм.Д3':<10}{C_VAL:>10.2f}{val_ln_norm:>16.8f}{ref_ln:>16.8f}{abs(val_ln_norm - ref_ln):>14.2e}{iter_ln_norm:>10}")
    print("=" * 85)