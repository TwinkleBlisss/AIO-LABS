import os
import time
import tsplib95
import numpy as np
import pandas as pd

from algorithms.knapsack_genetic import Knapsack
from algorithms.traveling_salesman_genetic import TSP


def test_values_knapsack(path: str = "benchmarks/knapsack/") -> dict:
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


def test_values_tsp(path: str = "benchmarks/tsp/") -> dict:
    def lower_diag_to_full_matrix(matrix: list[list]) -> list[list]:
        # записываем матрицу в список
        lower_diag_matrix_list = [
            matrix[i][j] for i in range(len(matrix))
            for j in range(len(matrix[i]))
        ]

        # приводим в нижне диагональную форму
        lower_diag_matrix = []
        row = []
        for i in range(len(lower_diag_matrix_list)):
            row.append(lower_diag_matrix_list[i])
            if lower_diag_matrix_list[i] == 0:
                lower_diag_matrix.append(row)
                row = []

        # делаем из неё симметричную матрицу
        tmp = pd.DataFrame(lower_diag_matrix)
        tmp = tmp.combine_first(tmp.T).values.tolist()
        # возвращаем нужный тип
        for i in range(len(tmp)):
            for j in range(len(tmp[i])):
                tmp[i][j] = int(tmp[i][j])
        return tmp

    def node_coord_to_full_matrix(tsp_problem: tsplib95.models.Problem) -> list[list]:
        dim = tsp_problem.dimension
        matrix = np.zeros((dim, dim))
        for i in range(dim):
            for j in range(dim):
                edge = i + 1, j + 1
                matrix[i][j] = tsp_problem.get_weight(*edge)
        return matrix.tolist()

    values = {}
    filenames = os.listdir(path) # список файлов в директории
    for file in filenames:
        if file != "optimal_solutions.txt":
            problem = tsplib95.load(path + file)
            test_name = problem.name
            values[test_name] = {}

            # записываем матрицу расстояний
            if problem.edge_weight_format == "LOWER_DIAG_ROW":
                values[test_name]["matrix"] = lower_diag_to_full_matrix(problem.edge_weights)
            if problem.edge_weight_type in ["EUC_2D", "ATT"]:
                values[test_name]["matrix"] = node_coord_to_full_matrix(problem)
            if problem.edge_weight_format == "FULL_MATRIX":
                values[test_name]["matrix"] = problem.edge_weights

    # записываем оптимальные решения
    with open(path + "optimal_solutions.txt", "r", encoding="utf8") as f:
        for line in f.readlines():
            test_name, opt_sol = line.split(" : ")
            values[test_name]["opt_sol"] = int(opt_sol[:len(opt_sol) - 1])

    return values


def get_output_and_time_knapsack(profits: list[int], weights: list[int], capacity: int):
    """
    Функция для получения решения и времени работы алгоритма на одном тесте.
    """
    start = time.time()
    chosen_items, profit = Knapsack(profits, weights, capacity).genetic_algorithm()
    end = time.time()
    return profit, chosen_items, (end - start) * 10**3


def get_output_and_time_tsp(distances):
    """
    Функция для получения решения и времени работы алгоритма на одном тесте.
    """
    start = time.time()
    best_route, best_length = TSP(distances).genetic_algorithm()
    end = time.time()
    return best_length, best_route, (end - start) * 10**3


def knapsack_results_on_tests():
    """
    Функция для вывода информации о работе алгоритма
    (результата и времени выполнения).
    """

    # загружаем тестовые данные
    knapsack_tests = test_values_knapsack()

    print("Knapsack genetic algorithm:")
    print('| {:^15} | {:^10} | {:^45} | {:^15} | {:^45} | {:^16} |'
          .format('Test name', 'Profit', 'Chosen items', 'Optimal profit',
                  'Optimal solution', 'Time in ms'))
    fmt = '| {:^15} | {:10} | {:^45} | {:15} | {:^45} | {:4.13f} |'
    for test_name, test_value in knapsack_tests.items():
        # оптимальное решение
        optimal_profit = sum([test_value['p'][i] if test_value['s'][i] == 1 else 0 for i in range(len(test_value['p']))])

        # решение алгоритма
        profit, chosen_items, algo_time = \
            get_output_and_time_knapsack(test_value['p'], test_value['w'], test_value['c'])

        print(fmt.format(test_name, profit, str(chosen_items),
                         optimal_profit, str(test_value['s']), algo_time))
    print("\n\n")


def tsp_results_on_tests():
    """
        Функция для вывода информации о работе алгоритма
        (результата и времени выполнения).
        """

    # загружаем тестовые данные
    tsp_tests = test_values_tsp()

    print("Traveling salesman problem genetic algorithm:")
    print('| {:^15} | {:^15} | {:^25} | {:^17} | {:^45} |'
          .format('Test name', 'Route length', 'Optimal route length',
                  'Time in ms', 'Route'))
    fmt = '| {:^15} | {:15} | {:25} | {:^4.15f} | {:^45} |'
    for test_name, test_value in tsp_tests.items():
        # решение алгоритма
        route_length, route, algo_time = \
            get_output_and_time_tsp(test_value['matrix'])

        print(fmt.format(test_name, route_length, test_value['opt_sol'],
                         algo_time, str(route)))
    print("\n\n")


def main():
    knapsack_results_on_tests()
    tsp_results_on_tests()


if __name__ == "__main__":
    main()
