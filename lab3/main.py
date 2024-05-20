# TODO: Написать загрузку тестов
import os
import time
import tsplib95
import pandas as pd


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

    values = {}
    filenames = os.listdir(path)
    for file in filenames:
        if file != 'optimal_solutions':
            problem = tsplib95.load(path + file)
            test_name = problem.name
            values[test_name] = {}
            if problem.edge_weight_format == 'LOWER_DIAG_ROW':
                values[test_name]['matrix'] = lower_diag_to_full_matrix(problem.edge_weights)
            # TODO: add optimal solution to dict "values"
            # TODO: add func to build matrix from node_coords(problem.get_edges() +
            #                                                 problem.get_weight(*edge))
    return values


def main():
    knapsack = test_values_knapsack()
    for test_name, test_value in knapsack.items():
        print(test_name)
        print(test_value)

    tsp = test_values_tsp()
    for test_name, test_value in tsp.items():
        print(test_name)
        print(test_value)


if __name__ == '__main__':
    main()
