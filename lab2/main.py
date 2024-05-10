import os
import time
# from algorithms.base import Base
from algorithms.dp_weights import DP_weights
from algorithms.ptas import PTAS
from algorithms.branch_and_bound import BranchAndBound
from algorithms.two_approx import TwoApprox

ALGORITHMS = [DP_weights, TwoApprox, BranchAndBound, PTAS]  # записать все классы алгоритмов (пока тестовый вариант)


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


def get_output_and_time(algorithm: [DP_weights | PTAS], *args) -> tuple[int, list[int], float, int]:
    """
    Функция для получения решения теста и времени работы алгоритма.
    :param algorithm: Класс алгоритма
    :param args: Параметры теста в формате (weights, profits, capacity)
    :return: Итоговый вес, итоговая стоимость, выбранный предметы, время работы
    """
    start = time.time()
    algo_class = algorithm(*args)
    algo_class.solve()
    profit, chosen_items, solution_number = algo_class.get_answer(), algo_class.get_items(), algo_class.get_solution_number()
    end = time.time()
    return profit, chosen_items, (end - start) * 10**3, solution_number


def check_algorithms(capacity: int, profits: list[int], optimal_solution: list[int], weights: list[int]) -> None:
    """
    Функция для вывода информации о работе алгоритма
    (результата, количества операций сравнения и времени выполнения).
    """
    print('| {:^15} | {:^10} | {:^35} | {:^15} | {:^35} | {:^15} | {:^16} |'
          .format('Algorithm', 'Profit', 'Chosen items', 'Optimal profit', 'Optimal solution', 'Time in ms', 'Num of solutions'))
    fmt = '| {:15} | {:10} | {:^35} | {:15} | {:^35} | {:4.13f} | {:^16} |'
    optimal_profit = sum([profits[i] if optimal_solution[i] == 1 else 0 for i in range(len(profits))])
    for algorithm in ALGORITHMS:
        profit, chosen_items, algo_time, solution_number = \
            get_output_and_time(algorithm, weights, profits, capacity)
        if len(profits) < 13:
            print(fmt.format(
                str(algorithm.__name__),
                profit,
                str(chosen_items),
                optimal_profit,
                str(optimal_solution),
                algo_time,
                solution_number
            ))
        else:
            # короткая запись ответов
            chosen_items_short = []
            optimal_solution_short = []
            for i in range(len(chosen_items)):
                if chosen_items[i] == 1:
                    chosen_items_short.append(i)
                if optimal_solution[i] == 1:
                    optimal_solution_short.append(i)
            print(fmt.format(
                str(algorithm.__name__),
                profit,
                str(chosen_items_short),
                optimal_profit,
                str(optimal_solution_short),
                algo_time,
                solution_number
            ))
    print()


def show_result() -> None:
    """
    Запуск на всех тестах.
    """
    # STATUS = "TEST ONE"
    STATUS = "FINAL"

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
