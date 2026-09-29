"""
Лабораторная работа. Вариант 4.
Алгоритм со сложностью O(n^(n*log n)).
Файл: main.py
"""

import math

def recursive_algorithm(n: int, current_depth: int) -> int:
    """
    Рекурсивная функция, формирующая дерево вызовов.
    Ветвление (branching factor) = n.
    """
    # Базовый случай: достигнут самый глубокий уровень дерева
    if current_depth <= 0:
        return 1
    
    operations = 0
    # Делаем n рекурсивных вызовов на каждом уровне
    for _ in range(n):
        operations += recursive_algorithm(n, current_depth - 1)
        
    return operations

def run_algorithm_O_n_n_logn(n: int) -> int:
    """
    Обертка для запуска алгоритма с вычислением необходимой глубины.
    """
    if n <= 1:
        return 1 # Для n=1 логарифм равен 0, сложность вырождается
        
    # Формируем глубину дерева как n * log(n)
    depth = int(n * math.log2(n))
    
    print(f"Параметры: n = {n}, ветвление = {n}, глубина = {depth}")
    
    # Запуск рекурсии
    result = recursive_algorithm(n, depth)
    
    print(f"Итоговое количество базовых операций (листьев дерева): {result}")
    return result

if __name__ == "__main__":
    # Демонстрация работы на малых n (из-за колоссальной скорости роста функции)
    print("--- Тест n = 2 ---")
    run_algorithm_O_n_n_logn(2)
    
    print("\n--- Тест n = 4 ---")
    run_algorithm_O_n_n_logn(4)