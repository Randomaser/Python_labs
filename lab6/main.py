"""
Лабораторная работа № 6. Вариант 4.
Двусвязный список с операциями дека (вставка с обоих концов) и история
переходов «вперёд-назад» на основе двусвязных узлов.
"""

import gc
import os
import platform
import statistics
import sys
import time

import matplotlib.pyplot as plt


SIZES = [2000, 4000, 8000]
REPEATS = 15
MEMORY_N = 10_000


class Node:
    """Узел двусвязного списка: значение и ссылки на соседние узлы."""
    __slots__ = ("value", "prev", "next")

    def __init__(self, value, prev=None, nxt=None):
        self.value = value
        self.prev = prev
        self.next = nxt


class DoublyLinkedDeque:
    """Дек на двусвязном списке: все операции с концов выполняются за Θ(1)."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def push_front(self, value):
        node = Node(value, None, self.head)
        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node
        self.head = node
        self.size += 1

    def push_back(self, value):
        node = Node(value, self.tail, None)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def pop_front(self):
        if self.head is None:
            raise IndexError("Дек пуст")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        self.size -= 1
        return node.value

    def pop_back(self):
        if self.tail is None:
            raise IndexError("Дек пуст")
        node = self.tail
        self.tail = node.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        self.size -= 1
        return node.value

    def to_list(self):
        """Содержимое от начала к концу."""
        result, node = [], self.head
        while node is not None:
            result.append(node.value)
            node = node.next
        return result

    def to_list_reversed(self):
        """Содержимое от конца к началу (проверка обратных ссылок)."""
        result, node = [], self.tail
        while node is not None:
            result.append(node.value)
            node = node.prev
        return result

    def clear(self):
        """Освобождает узлы, разрывая циклические ссылки prev/next (без этого память освобождает только GC)."""
        node = self.head
        while node is not None:
            nxt = node.next
            node.prev = None
            node.next = None
            node = nxt
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size


class BrowserHistory:
    """История переходов: текущая страница и цепочки назад/вперёд."""

    def __init__(self, homepage):
        self.head = Node(homepage)
        self.current = self.head

    def visit(self, page):
        """Новый переход: цепочка «вперёд» отрезается, новая страница добавляется."""
        new = Node(page, self.current, None)
        self.current.next = new
        self.current = new

    def back(self):
        if self.current.prev is not None:
            self.current = self.current.prev
        return self.current.value

    def forward(self):
        if self.current.next is not None:
            self.current = self.current.next
        return self.current.value

    def pages(self):
        """Все страницы цепочки от начальной до последней (включая «вперёд»)."""
        result, node = [], self.head
        while node is not None:
            result.append(node.value)
            node = node.next
        return result


def build_list(n: int, front: bool) -> list:
    """Строит list из n элементов вставкой в начало или в конец."""
    data = []
    for i in range(n):
        if front:
            data.insert(0, i)
        else:
            data.append(i)
    assert len(data) == n
    return data


def build_deque(n: int, front: bool) -> DoublyLinkedDeque:
    """Строит дек из n элементов вставкой в начало или в конец."""
    deque = DoublyLinkedDeque()
    for i in range(n):
        if front:
            deque.push_front(i)
        else:
            deque.push_back(i)
    assert len(deque) == n
    return deque


def clear_deque(deque: DoublyLinkedDeque) -> None:
    """Очистка дека после замера: разрывает циклы, чтобы память не оставалась мусору для GC."""
    deque.clear()


def measure(build, cleanup=None) -> float:
    """Медиана времени build() за REPEATS запусков, с.
    Перед каждым запуском GC очищает память, во время замера GC отключён,
    после замера результат удаляется функцией cleanup."""
    times = []
    for _ in range(REPEATS):
        gc.collect()
        gc.disable()
        try:
            started = time.perf_counter()
            obj = build()
            times.append(time.perf_counter() - started)
        finally:
            gc.enable()
        if cleanup is not None:
            cleanup(obj)
    return statistics.median(times)


def memory_of_list(data: list) -> int:
    """Память списка: контейнер и объекты-элементы, байт."""
    return sys.getsizeof(data) + sum(sys.getsizeof(x) for x in data)


def memory_of_deque(deque: DoublyLinkedDeque) -> int:
    """Память дека: каждый узел (с учётом слотов) и объекты значений, байт."""
    total = sys.getsizeof(deque)
    node = deque.head
    while node is not None:
        total += sys.getsizeof(node) + sys.getsizeof(node.value)
        node = node.next
    return total


def correctness_demo() -> None:
    """Т1: проверка дека и истории на малом примере с выводом после каждой операции."""
    print("Т1. Дек: проверка на малом примере")
    deque = DoublyLinkedDeque()
    steps = [
        ("push_back", "B"), ("push_back", "C"), ("push_front", "A"),
        ("push_front", "Z"), ("pop_back", None), ("pop_front", None),
    ]
    for op, arg in steps:
        if op == "pop_back":
            result = deque.pop_back()
        elif op == "pop_front":
            result = deque.pop_front()
        else:
            getattr(deque, op)(arg)
            result = None
        suffix = f" -> извлечено {result!r}" if result is not None else ""
        print(f"  {op}({arg or ''}){suffix}: вперёд {deque.to_list()}, назад {deque.to_list_reversed()}")
    assert deque.to_list() == deque.to_list_reversed()[::-1]

    print("\nТ1. История переходов")
    history = BrowserHistory("home")
    for page in ["news", "mail", "shop"]:
        history.visit(page)
    print(f"  после переходов: текущая = {history.current.value}, цепочка = {history.pages()}")
    print(f"  back -> {history.back()}, back -> {history.back()}")
    print(f"  forward -> {history.forward()}")
    history.back()
    history.back()
    history.visit("blog")
    print(f"  visit(blog) после возврата: текущая = {history.current.value}, цепочка = {history.pages()}")
    assert history.forward() == "blog"
    assert history.pages() == ["home", "blog"]


def experiment() -> dict:
    """Замеры вставки в начало и в конец для дека и list."""
    results = {}
    for n in SIZES:
        results[n] = {
            "deque_front": measure(lambda: build_deque(n, front=True), clear_deque),
            "list_front": measure(lambda: build_list(n, front=True)),
            "deque_back": measure(lambda: build_deque(n, front=False), clear_deque),
            "list_back": measure(lambda: build_list(n, front=False)),
        }
    return results


def memory_experiment() -> dict:
    """Т4: расход памяти на MEMORY_N элементов."""
    values = list(range(MEMORY_N))
    deque = DoublyLinkedDeque()
    for value in values:
        deque.push_back(value)
    return {
        "list": memory_of_list(values),
        "deque": memory_of_deque(deque),
    }


def save_chart(results: dict) -> None:
    """Сохраняет график T(n) для вставки в начало и в конец."""
    out_dir = os.path.dirname(os.path.abspath(__file__))
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, side, title in ((axes[0], "front", "Вставка в начало"), (axes[1], "back", "Вставка в конец")):
        ax.plot(SIZES, [results[n][f"deque_{side}"] for n in SIZES], "o-", label="Двусвязный дек (Θ(1) на вставку)")
        list_label = "list (Θ(n) на вставку в начало)" if side == "front" else "list (амортизированно Θ(1) в конец)"
        ax.plot(SIZES, [results[n][f"list_{side}"] for n in SIZES], "s-", label=list_label)
        ax.set_xlabel("n — число вставок")
        ax.set_ylabel("Время построения, с")
        ax.set_title(title)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "lr6_time.png"), dpi=160)
    plt.close(fig)


def main() -> None:
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"ОС: {platform.platform()}; логических процессоров: {os.cpu_count()}\n")

    correctness_demo()

    print(f"\nЗамеры: время построения структуры из n элементов, с (медиана {REPEATS} запусков)")
    results = experiment()
    print(f"{'n':>6} | {'дек, в начало':>14} | {'list, в начало':>15} | {'дек, в конец':>13} | {'list, в конец':>14}")
    print("-" * 75)
    for n in SIZES:
        r = results[n]
        print(f"{n:>6} | {r['deque_front']:>14.6f} | {r['list_front']:>15.6f} | "
              f"{r['deque_back']:>13.6f} | {r['list_back']:>14.6f}")

    print("\nОтношение T(2n)/T(n)")
    for key in ("deque_front", "list_front", "deque_back", "list_back"):
        ratios = [results[SIZES[i + 1]][key] / results[SIZES[i]][key] for i in range(len(SIZES) - 1)]
        print(f"  {key:<12}: " + ", ".join(f"{r:.2f}" for r in ratios))

    print(f"\nТ4. Память на {MEMORY_N} элементов (sys.getsizeof)")
    memory = memory_experiment()
    print(f"  list: {memory['list']} байт, дек на узлах: {memory['deque']} байт, "
          f"отношение {memory['deque'] / memory['list']:.2f}")

    save_chart(results)
    print("\nГрафик сохранён: lr6_time.png")


if __name__ == "__main__":
    main()
