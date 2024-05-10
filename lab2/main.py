import os
import time
# from algorithms.base import Base
from algorithms.dp_weights import DP_weights
from algorithms.ptas import PTAS

ALGORITHMS = [PTAS]  # записать все классы алгоритмов (пока тестовый вариант)


def test_values(path: str = "benchmarks/") -> dict:
    values = {}
    tests_numbers = os.listdir(path)
    for tests_number in tests_numbers:
        test_name = f"Test {tests_number}"
        values[test_name] = {}
        filenames = os.listdir(path + tests_number)
        for filename in filenames:
            with open(path + tests_number + "/" + filename, "r", encoding="utf8") as f:
                if filename[0] == "c":
                    values[test_name][filename[0]] = int(f.read())
                else:
                    values[test_name][filename[0]] = [int(line) for line in f.readlines()]
    return values


def get_output_and_time(algorithm: [DP_weights | PTAS], *args) -> tuple[int, int, list[int], float]:
    """
    Функция для получения решения теста и времени работы алгоритма.
    :param f: Класс алгоритма
    :param args: Параметры теста в формате (weights, profits, capacity)
    :return: Итоговый вес, итоговая стоимость, выбранный предметы, время работы
    """
    start = time.time()
    algo_class = algorithm(*args)
    algo_class.solve()
    profit, chosen_items = algo_class.get_answer(), algo_class.get_items()
    end = time.time()
    return 666, profit, chosen_items, (end - start)


def check_algorithms(capacity: int, profits: list[int], optimal_solution: list[int], weights: list[int]) -> None:
    """
    Функция для вывода информации о работе алгоритма
    (результата, количества операций сравнения и времени выполнения).
    """
    print('{:10} | {:7} | {:7} | {:^35} | {:^35} | {:^12}'
          .format('Algorithm', 'Weight', 'Profit', 'Chosen items', 'Optimal solution', 'Time in sec'))
    fmt = '{:10} | {:7} | {:7} | {:35} | {:35} | {:.10f}'
    for algorithm in ALGORITHMS:
        weight, profit, chosen_items, algo_time = \
            get_output_and_time(algorithm, weights, profits, capacity)
        print(fmt.format(
            str(algorithm.__name__), weight, profit,
            str(chosen_items),
            str(optimal_solution),
            algo_time
        ))
    print()


def show_result() -> None:
    """
    Запуск на всех тестах.
    """
    # STATUS = "TEST ONE"
    STATUS =  "FINAL"

    tests = test_values()
    for test_name, test_value in tests.items():
        print(test_name)
        if STATUS == "TEST ONE":
            dp = DP_weights(test_value['w'], test_value['p'], test_value['c'])
            start = time.time()
            dp.solve()
            print("Items", dp.get_items())
            print("Answer", dp.get_answer())
            end = time.time()
            fmt = "{:.10f}"
            print(fmt.format((end - start)), "c")
        else:
            check_algorithms(test_value['c'], test_value['p'], test_value['s'], test_value['w'])


def main():
    show_result()


if __name__ == '__main__':
    main()
