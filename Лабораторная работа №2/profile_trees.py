import timeit
import matplotlib.pyplot as plt
from recursive_tree import gen_bin_tree_recursive
from iterative_tree import gen_bin_tree_iterative


def setup_data(n: int) -> list:
    return [(i, n) for i in range(1, n + 1)]  # Генерация пар (root, height)


def calculate_time(root: int, height: int, func) -> float:
    delta = 0
    # Запуск функции несколько раз для усреднения времени
    for _ in range(100):  # 100 прогонов
        start_time = timeit.default_timer()
        func(root, height)
        delta += timeit.default_timer() - start_time
    return delta / 100  # Возвращаем усреднённое время


def main():
    heights = list(range(1, 6))  # Высоты от 1 до 5
    recursive_times = []
    iterative_times = []

    for height in heights:
        avg_recursive_time = calculate_time(2, height, gen_bin_tree_recursive)
        recursive_times.append(avg_recursive_time)

        avg_iterative_time = calculate_time(2, height, gen_bin_tree_iterative)
        iterative_times.append(avg_iterative_time)

    # Визуализация
    plt.plot(heights, recursive_times, label='Рекурсивное построение', marker='o')
    plt.plot(heights, iterative_times, label='Нерекурсивное построение', marker='o')
    plt.xlabel('Высота дерева')
    plt.ylabel('Среднее время выполнения (сек)')
    plt.title('Сравнение рекурсивного и нерекурсивного построения дерева')
    plt.legend()
    plt.grid()
    plt.savefig('tree_comparison.png')
    plt.show()


if __name__ == "__main__":
    main()
